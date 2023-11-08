import yaml
import json
import pdb


br = pdb.set_trace

#fn = '../user-Alice/questions/230330.Questions.yaml'
fn = '../user-Alice/questions/230327.OP-TEE.yaml'
f = open(fn)
qs = yaml.load(f, Loader=yaml.loader.SafeLoader)
f.close()

print(json.dumps(qs, indent=4))

br()