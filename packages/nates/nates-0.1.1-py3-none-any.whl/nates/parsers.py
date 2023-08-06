import pandas as pd 

class Sentence():
	def __init__(self, sent):
		self.sent = sent

	def bundle(self, bundle_f, **kwargs):
		return self._bundle(self.sent, bundle_f, **kwargs)

	def _bundle(self, sent, bundle_f):
		bundle_map = {}
		for tok in sent:
			i = bundle_f(tok)
			bundle_map[tok.i] = i if i is not None else i

		bundles = {}
		for tok in sent:  
			i = tok.i
			while bundle_map[i] != i:
				i = bundle_map[i]
			bundles[i] = bundles.get(i, []) + [tok]

		bundles = pd.Series(bundles).reset_index().rename(columns={'index': 'id', 0: 'value'})
		return bundles

	def generate_token_table(self, **kwargs):
		return self._generate_token_table(self.sent, **kwargs)

	def _generate_token_table(self, sent, features={}, subset=None):
		data = []
		for tok in self.sent:
			row = {
					'id': tok.i,
					'tok': tok,
					'pos': tok.pos_,
					'dep': tok.dep_,
					'tag': tok.tag_,
					'head': tok.head,
					'ancestors': list(tok.ancestors),
					'children': list(tok.children),
					'subtree': list(tok.subtree),
			}
			data.append(row)
		data = pd.DataFrame(data)
		default_cols = [x for x in data.columns if x not in ['id', 'tok']]

		if subset is not None:
			data = data[[x for x in data.columns if x in ['id', 'tok'] + subset]]

		for name, feature in features.items():
			data = data.merge(feature, on='id', how='left').rename(columns={'value': name})

		return data[[x for x in data.columns if x not in default_cols] + [x for x in data.columns if x in default_cols]]