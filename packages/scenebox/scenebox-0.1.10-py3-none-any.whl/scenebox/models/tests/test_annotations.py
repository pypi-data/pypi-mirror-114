import numpy as np
from shared.external.models.annotation import MRCNNAnnotation


def test_create_mrcnn_annotation():
    annotation_id = "dd0f5995-ec1d-43fa-bfc8-f8a1f9c7b9fe_frame_0.ann"
    media_asset_id = "dd0f5995-ec1d-43fa-bfc8-f8a1f9c7b9fe_frame_0.png"
    formatted_response = {
        'labels': ['car'],
        'masks': None,
        'bounding_boxes': np.array([[467, 448, 487, 485], ], dtype=np.int32),
        'confidences': np.array([0.99512035], dtype=np.float32),
        'resolution': None
    }
    annotation_binary_id = "2b17d2fc-ae58-4df0-becd-4bdf6c2efd1b.ann"
    destination_set = None

    annotation = MRCNNAnnotation(
        id=annotation_id,
        media_asset_id=media_asset_id,
        file_labels=formatted_response,
        annotation_binary_id=annotation_binary_id,
        destination_set=destination_set)

    assert annotation.id == annotation_id
    assert annotation.annotation_type == 'two_d_bounding_box'
    assert annotation.ground_truth == 'false'
    assert annotation.inference_labelling_model == 'mrcnn'
    assert annotation.file_labels == formatted_response
    annotation_dict = annotation.to_dic()
    annotation_entities = annotation_dict['annotation_entities']
    annotation_entities[0].pop("uid")
    assert annotation_entities == \
        [
            {
                'annotation_type': 'two_d_bounding_box',
                'attributes': {},
                'category_id': None,
                'confidence': 0.9951203465461731,
                'coordinates': [{'x': 448.0, 'y': 467.0},
                                {'x': 485.0, 'y': 467.0},
                                {'x': 485.0, 'y': 487.0},
                                {'x': 448.0, 'y': 487.0}],
                'label': 'car',
                'related_annotations': []
            }
        ]
