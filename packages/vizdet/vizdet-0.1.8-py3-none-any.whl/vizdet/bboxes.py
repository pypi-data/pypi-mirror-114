from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Sequence, Tuple, Union

import cv2  # type: ignore
import numpy as np

from .font import Font

# Default color list
VIBRANT_COLOR_LIST = (
    (238, 119, 51),
    (0, 118, 187),
    (51, 188, 238),
    (238, 51, 120),
    (204, 51, 17),
    (0, 153, 135),
    (187, 187, 187),
)

# Common colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class ColorMode(Enum):
    """Determines what the color of the bounding box is based on."""

    LABELS = 1
    IDS = 2


@dataclass
class BBoxes:
    """The class for drawing bounding boxes and associated labels of detected objects.

    Args:
        font: The label font. If not set, the default font will be used.
        labels_list: A list of possible labels. If set, the labels passed to the
            :meth:`~.draw_boxes` method should be integer indices corresponding to
            the labels in ``labels_list``. These (text) labels will then be drawn.
        text_color: Color of the label text.
        bbox_color_list: A list of colors in RGB format to use for bounding boxes.
        color_mode: Whether to color bounding boxes based in class or item ids.
        box_thickness: Thickness of the bounding box.
        padding: How many pixels to pad the label background on each side.
        separator: What to separate different parts of the text label with
        font_height: Label font height.
    """

    font: Font = field(default_factory=Font.get_default)
    labels_list: Optional[Sequence[str]] = None
    text_color: Tuple[int, int, int] = BLACK
    bbox_color_list: Sequence[Tuple[int, int, int]] = VIBRANT_COLOR_LIST
    color_mode: ColorMode = ColorMode.LABELS
    box_thickness: int = 2
    padding: int = 2
    separator: str = " | "
    font_height: int = 15

    def _get_label_value(
        self, label: Optional[Union[int, str]]
    ) -> Optional[Union[str, int]]:
        """Get value of the label in ``labels_list``, if set up."""

        if self.labels_list and label is not None:
            if not isinstance(label, (int, np.integer)):
                raise TypeError(
                    f"Label `{label}` is not an integer; if you supply"
                    " `label_list`, then labels must be integer indices."
                )

            try:
                return self.labels_list[label]
            except IndexError:
                raise IndexError(
                    f"Label index `{label}` is not value for `labels_list`"
                    f" of length {len(self.labels_list)}"
                )

        return label

    def _get_text_label(
        self,
        item_id: Optional[int] = None,
        label: Optional[Union[str, int]] = None,
        score: Optional[float] = None,
        misc: Optional[str] = None,
    ) -> Optional[str]:
        """Get the text label to draw by combining object info.

        Args:
            item_id: The ID of the object (from tracking).
            label: The label of the object.
            score: The confidence score (probability) of the label.
            misc: Any other text to display.

        Returns:
            The elements of the label concatenated by the separator.
        """

        if not any(x is not None for x in (item_id, label, score, misc)):
            return None

        id_str, label_str = None, None
        if item_id is not None:
            id_str = f"#{item_id}"
        if label is not None:
            label_str = str(self._get_label_value(label))
        if score is not None:
            if label_str:
                label_str = f"{label_str}: {score:.2f}"
            else:
                label_str = f"{score:.2f}"

        return self.separator.join(filter(None, (id_str, label_str, misc)))

    def _get_bbox_color(
        self,
        label: Optional[Union[str, int]],
        item_id: Optional[int],
    ) -> Tuple[int, int, int]:
        """Get the color of the box, based on label (hash) or item id."""

        color_ind: Optional[int] = None
        if self.color_mode == ColorMode.LABELS:
            if isinstance(label, str):
                color_ind = abs(hash(label))
            elif isinstance(label, (int, np.integer)):
                color_ind = label
        elif self.color_mode == ColorMode.IDS:
            color_ind = item_id

        return self.bbox_color_list[(color_ind or 0) % len(self.bbox_color_list)]

    def _get_text_bbox_params(
        self, label: str, box_orig: Tuple[int, int], font_height: int
    ) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
        """Get the label and background positional params.

        Returns:
            A tuple containing:

                text_orig: The coordinates of the bottom-left cornet
                    of the text label
                box_pt1: The first point of the text background box
                box_pt2: The second point of the text background box
        """

        bsize = self.font.font.getTextSize(label, font_height, -1)

        text_orig = (
            box_orig[0] + self.padding,
            box_orig[1] - bsize[1] - self.padding,
        )
        box_pt1 = (
            box_orig[0] - self.box_thickness // 2,
            box_orig[1] - bsize[0][1] - bsize[1] - 2 * self.padding,
        )
        box_pt2 = (
            box_orig[0] + bsize[0][0] + 2 * self.padding,
            box_orig[1] + self.box_thickness // 2,
        )

        return text_orig, box_pt1, box_pt2

    def draw(
        self,
        img: np.ndarray,
        bboxes: Union[Sequence[Tuple[int, int, int, int]], np.ndarray],
        ids: Union[Optional[Sequence[int]], np.ndarray] = None,
        labels: Union[Optional[Sequence[Union[str, int]]], np.ndarray] = None,
        scores: Union[Optional[Sequence[float]], np.ndarray] = None,
    ):
        """Draw the bounding boxes with their labels.

        The bounding boxes are drawn as specified in ``bboxes``, and
        the label is drawn on the upper left part of the box. Any object
        information (label, item IDs for tracking, label scores) will
        be added to the label, and separated by "|".

        The color of the boxes depends either on the labels or item IDs, as
        was specified in ``color_mode``. If the color depends on labels,
        and labels are passed as strings, their contents will be hashed to
        obtain a numeric index in the color list.

        If ``labels_list`` was set, then ``labels`` should be integer
        indices, and the value displayed will be the string from ``labels_list``
        corresponding to the index.

        This method edits the ``img`` in place and does not return any value.

        Args:
            img: The image to draw bounding boxes on.
            bboxes: Coordinates of bounding boxes in the
                ``[xmin, ymin, xmax, ymax]`` format. Elements should be integers.
            ids: Item IDs from tracking.
            labels: Item labels (classes). If ``labels_list`` is set labels
                should be intigers corresponding to indices of that list.
            scores: The confidence (probability) of the label, should
                be a floating-point number between 0 and 1.
        """

        # Check that all lists are of proper size
        if ids is not None and len(ids) != len(bboxes):
            raise ValueError(
                "The `ids` should be the same lenght as the `boxes_coords`."
            )

        if labels is not None and len(labels) != len(bboxes):
            raise ValueError(
                "The `labels` should be the same lenght as the `boxes_coords`."
            )

        if scores is not None and len(scores) != len(bboxes):
            raise ValueError(
                "The `scores` should be the same lenght as the `boxes_coords`."
            )

        if not isinstance(bboxes[0][0], (int, np.integer)):
            raise ValueError("The `bboxes` elements should be integers.")

        for idx, coords in enumerate(bboxes):
            # Get the label and color of the box
            item_id = ids[idx] if ids is not None else None
            label = labels[idx] if labels is not None else None
            score = scores[idx] if scores is not None else None

            text_label = self._get_text_label(item_id, label, score)
            bbox_color = self._get_bbox_color(label, item_id)

            # Draw object bounding box
            _ = cv2.rectangle(
                img,
                pt1=(coords[0], coords[1]),
                pt2=(coords[2], coords[3]),
                color=bbox_color[::-1],
                thickness=self.box_thickness,
            )

            # Draw label-related things
            if text_label:
                text_org, text_box_pt1, text_box_pt2 = self._get_text_bbox_params(
                    text_label, coords[0:2], self.font_height
                )

                cv2.rectangle(
                    img,
                    pt1=text_box_pt1,
                    pt2=text_box_pt2,
                    color=bbox_color[::-1],
                    thickness=-1,
                )
                self.font.font.putText(
                    img=img,
                    text=text_label,
                    org=text_org,
                    fontHeight=self.font_height,
                    color=self.text_color[::-1],
                    thickness=-1,
                    line_type=cv2.LINE_AA,
                    bottomLeftOrigin=True,
                )
