# search a dict in a list of dicts
from pprint import pprint


def has_value(obj, val):
	if isinstance(obj, dict):
		values = obj.values()
	elif isinstance(obj, list):
		values = obj
	if val in values:
		return True
	for v in values:
		if isinstance(v, (dict, list)) and has_value(v, val):
			return True
	return False


a = {
	'metadata': {
		'moderation_service_version': '0.4.11', 'text_taxonomy_version': '0.1.2'}, 'total': 2, 'violations': [
		{'asset_type': 'text',
		 'confidence': [{'child_label': 'Hateful', 'score': 0.985709, 'threshold_considered': 0.2},
						{'child_label': 'Racist', 'score': 0.747528, 'threshold_considered': 0.2}],
		 'moderation_category': 'offensive', 'reason': 'Offensive content targeting race, religion etc'},
		{'asset_type': 'text',
		 'confidence': [{'child_label': 'Inappropriate', 'score': 0.974816, 'threshold_considered': 0.2},
						{'child_label': 'Obscene', 'score': 0.988402, 'threshold_considered': 0.2},
						{'child_label': 'Profanity', 'score': 0.996858, 'threshold_considered': 0.2}],
		 'moderation_category': 'profanity', 'reason': 'Obscene language, masked profanity'}]
}

b = {'metadata': {'moderation_service_version': '0.4.11', 'text_taxonomy_version': '0.1.2'}, 'total': 2, 'violations': [
	{'asset_type': 'text',
	 'confidence': [{'child_label': 'Inappropriate', 'score': 0.974816, 'threshold_considered': 0.2},
					{'child_label': 'Obscene', 'score': 0.988402, 'threshold_considered': 0.2},
					{'child_label': 'Profanity', 'score': 0.996858, 'threshold_considered': 0.2}],
	 'moderation_category': 'profanity', 'reason': 'Obscene language, masked profanity'},
	{'asset_type': 'text',
	 'confidence': [{
		 'child_label': 'Hateful',
		 'score': 0.985709,
		 'threshold_considered': 0.2},
		 {
			 'child_label': 'Racist',
			 'score': 0.747528,
			 'threshold_considered': 0.2}],
	 'moderation_category': 'offensive',
	 'reason': 'Offensive content targeting race, religion etc'}]}

for item in a["violations"]:
	pprint(item)
	assert has_value(b["violations"], item)