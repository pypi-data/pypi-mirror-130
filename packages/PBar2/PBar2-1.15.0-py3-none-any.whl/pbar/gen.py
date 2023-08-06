from typing import Callable, Optional, Union
from enum import Enum, auto

from . import sets, utils
from . utils import Term, capValue



class Gfrom(Enum):
	"""Enum for the different ways to generate a bar."""
	AUTO = auto()
	LEFT = auto()
	RIGHT = auto()
	TOP = auto()
	BOTTOM = auto()
	CENTER_X = auto()
	CENTER_Y = auto()


class BarContent:
	"""
	Generate the content of the bar.
	Call this object to get the content string with the properties supplied.
	"""
	def __init__(self, gfrom: Gfrom, invert: bool = True) -> None:
		"""@gfrom: Place from where the full part of the bar will grow."""
		self.gfrom = gfrom
		self.invert = invert


	def __call__(self,
			position: tuple[int, int], size: tuple[int, int],
			charset: tuple[str, str], parsedColorset, prange: tuple[int, int]
		) -> str:
		"""Generate the content of the bar."""
		if self.gfrom == Gfrom.AUTO:
			self.gfrom = Gfrom.LEFT if size[0]/2 > size[1] else Gfrom.BOTTOM

		if self.gfrom in {Gfrom.LEFT, Gfrom.RIGHT, Gfrom.CENTER_X}:
			genFunc: Callable = self._genHoriz
		elif self.gfrom in {Gfrom.TOP, Gfrom.BOTTOM, Gfrom.CENTER_Y}:
			genFunc: Callable = self._genVert
		else:
			raise RuntimeError(f"unknown gfrom {self.gfrom!r}")

		setEntry = ("empty", "full") if self.invert else ("full", "empty")

		return genFunc(
			position, size,
			(charset[setEntry[0]], charset[setEntry[1]]),
			(parsedColorset[setEntry[0]], parsedColorset[setEntry[1]]),
			prange
		)


	def _genHoriz(self, pos, size, chars, colors, prange) -> str:
		width, height = size
		charFull, charEmpty = chars
		colorFull, colorEmpty = colors
		SEGMENTS_FULL = int((prange[0] / prange[1])*width)
		SEGMENTS_EMPTY = width - SEGMENTS_FULL

		"""
		When drawing horizontally:
			1. Print the full character the number of SEGMENTS_FULL.
			2. Print the empty character the number of SEGMENTS_EMPTY.
			3. Duplicate for each row of the bar.
		"""

		def iterRows(string: str):
			return "".join((
				Term.pos(pos, (0, row))
				+ string
			) for row in range(height))

		if self.gfrom == Gfrom.LEFT:
			return iterRows(
				colorFull + charFull*SEGMENTS_FULL
				+ colorEmpty + charEmpty*SEGMENTS_EMPTY
			)
		elif self.gfrom == Gfrom.RIGHT:
			return iterRows(
				colorEmpty + charEmpty*SEGMENTS_EMPTY
				+ colorFull + charFull*SEGMENTS_FULL
			)
		elif self.gfrom == Gfrom.CENTER_X:
			"""
			For the center:
				1. Print the entire empty bar.
				2. Move the cursor left to the center + half SEGMENTS_FULL.
				3. Print the completed bar chars.
			"""
			return iterRows(
				colorEmpty + charEmpty*width
				+ Term.moveHoriz(-width/2 - SEGMENTS_FULL/2)
				+ colorFull + charFull*SEGMENTS_FULL
			)


	def _genVert(self, pos, size, chars, colors, prange) -> str:
		width, height = size
		charFull, charEmpty = chars
		colorFull, colorEmpty = colors
		SEGMENTS_FULL = int(capValue((prange[0] / prange[1])*height, max=height))
		SEGMENTS_EMPTY = capValue(height - SEGMENTS_FULL, min=0)

		"""
		When drawing vertically, we esentially:
			1. Print one full row with the width of the bar.
			2. Move the cursor one character down, and the width of the bar to the left.
			3. Repeat
		"""

		if self.gfrom == Gfrom.TOP:
			return (
				Term.pos(pos)
				+ colorFull + (charFull*width + Term.posRel((-width, 1)))*SEGMENTS_FULL
				+ colorEmpty + (charEmpty*width + Term.posRel((-width, 1)))*SEGMENTS_EMPTY
			)
		elif self.gfrom == Gfrom.BOTTOM:
			return (
				Term.pos(pos)
				+ colorEmpty + (charEmpty*width + Term.posRel((-width, 1)))*SEGMENTS_EMPTY
				+ colorFull + (charFull*width + Term.posRel((-width, 1)))*SEGMENTS_FULL
			)
		elif self.gfrom == Gfrom.CENTER_Y:
			"""
			For the center:
				1. Print the entire empty bar.
				2. Move the cursor up to the center + half SEGMENTS_FULL.
				3. Print the completed bar rows.
			"""
			return (
				Term.pos(pos)
				+ colorEmpty + (charEmpty*width + Term.posRel((-width, 1)))*height
				+ Term.moveVert(-height/2 - SEGMENTS_FULL/2)
				+ colorFull + (charFull*width + Term.posRel((-width, 1)))*SEGMENTS_FULL
			)




def shape(
		position: tuple[int, int], size: tuple[int, int], charset,
		parsedColorset: dict, filled: Optional[str] = " "
	) -> str:
	"""Generates a basic rectangular shape that uses a charset and a parsed colorset"""
	width, height = size[0] - 2, size[1] - 1

	charVert = (	# Vertical characters, normally "|" at both sides.
		parsedColorset["vert"]["left"] + charset["vert"]["left"],
		parsedColorset["vert"]["right"] + charset["vert"]["right"]
	)
	charHoriz = (	# Horizontal characters, normally "-" at top and bottom. Colors are not specified here to not spam output
		charset["horiz"]["top"],
		charset["horiz"]["bottom"],
	)
	charCorner = (	# Corners of the shape at all four sides
		parsedColorset["corner"]["tleft"] + charset["corner"]["tleft"],
		parsedColorset["corner"]["tright"] + charset["corner"]["tright"],
		parsedColorset["corner"]["bleft"] + charset["corner"]["bleft"],
		parsedColorset["corner"]["bright"] + charset["corner"]["bright"]
	)


	top: str = (
		Term.pos(position)
		+ charCorner[0]
		+ parsedColorset["horiz"]["top"] + charHoriz[0]*width
		+ charCorner[1]
	)

	mid: str = "".join((	# generate all the rows of the bar. If filled is None, we just make the cursor jump to the right
		Term.pos(position, (0, row+1))
		+ charVert[0]
		+ (Term.moveHoriz(width) if filled is None else filled[0]*width)
		+ charVert[1]
	) for row in range(height))

	bottom: str = (
		Term.pos(position, (0, height))
		+ charCorner[2]
		+ parsedColorset["horiz"]["bottom"] + charHoriz[1]*width
		+ charCorner[3]
	)

	return top + mid + bottom




def bText(
		position: tuple[int, int], size: tuple[int, int],
		parsedColorset: dict[str, Union[dict, str]], formatset: sets.FormatSet
	) -> str:
	"""Generates all text for the bar"""
	width, height = size

	# set the max number of characters that a string should have on each part of the bar
	txtMaxWidth = width + 2
	txtSubtitle = utils.stripText(formatset["subtitle"], txtMaxWidth)
	txtInside = utils.stripText(formatset["inside"], txtMaxWidth - 4)
	txtTitle = utils.stripText(formatset["title"], txtMaxWidth)

	# position each text on its correct position relative to the bar
	textTitle = (
		Term.pos(position, (-1, 0))
		+ parsedColorset["text"]["title"]
		+ txtTitle
	)

	textSubtitle = (
		Term.pos(position, (width - len(txtSubtitle) + 1, height - 1))
		+ parsedColorset["text"]["subtitle"]
		+ txtSubtitle
	)

	textRight = (
		Term.pos(position, (width + 3, height/2))
		+ parsedColorset["text"]["right"]
		+ formatset["right"]
	) if formatset["right"] else ""

	textLeft = (
		Term.pos(position, (-len(formatset["left"]) - 3, height/2))
		+ parsedColorset["text"]["left"]
		+ formatset["left"]
	) if formatset["left"] else ""

	textInside = (
		Term.pos(position, (width/2 - len(txtInside)/2, height/2))
		+ parsedColorset["text"]["inside"]
		+ txtInside
	)

	return textTitle + textSubtitle + textRight + textLeft + textInside




def rect(
		pos: tuple[int, int], size: tuple[int, int],
		char: str="█", color: utils.Color="white"
	) -> str:
	"""Generate a rectangle."""
	return shape(
		pos, size,
		sets.CharSet({"corner": char, "horiz": char, "vert": char}),
		sets.ColorSet({"corner": color, "horiz": color, "vert": color}).parsedValues(),
		char
	)