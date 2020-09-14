import pdb
import pandas as pd

def make_set(df, source,target):
	source_dat = ["<"+source+"> " + x + " <"+target+">" for x in df[source]]
	target_dat = df[target]
	return pd.DataFrame({(source + "s"): source_dat, (target + "t"):target_dat})

data = {}
for lset in ["train","dev","test"]:
	baselangs = {}
	for lang in ["fr","en"]:
		sublangs = {}
		bam = open("../data/raw_"+lang+"_bam/"+lset+".bam")
		sublangs["bam"] = [x.strip() for x in bam.readlines()]
		leuro = open("../data/raw_"+lang+"_bam/"+lset+"."+lang)
		sublangs[lang] = [x.strip() for x in leuro.readlines()]
		baselangs[lang] = sublangs
	data[lset] = baselangs
	ftb = pd.DataFrame(data[lset]['fr'])
	etb = pd.DataFrame(data[lset]['en'])
	etf = ftb.set_index("bam").join(etb.set_index("bam"),how="inner")

	output = {"fr": {}, "en": {}, "bam": {}}
	output["fr"]["fr"] = make_set(ftb,"fr","fr")
	output["fr"]["en"] = make_set(etf,"fr","en")
	output["fr"]["bam"] = make_set(ftb,"fr","bam")

	output["bam"]["fr"] = make_set(ftb,"bam","fr")
	output["bam"]["en"] = make_set(etb,"bam","en")
	output["bam"]["bam"] = make_set(ftb,"bam","bam")

	output["en"]["fr"] = make_set(etf,"en","fr")
	output["en"]["en"] = make_set(etb,"en","en")
	output["en"]["bam"] = make_set(etb,"en","bam")

	sources = []
	targets = []
	langs = ['en','bam','fr']

	if lset == "train":
		for l1 in langs:
			for l2 in langs:
				sources = sources + list(output[l1][l2][l1+"s"])
				targets = targets + list(output[l1][l2][l2+"t"])
	else:
		sources = list(output["bam"]["fr"]["bams"])
		targets = list(output["bam"]["fr"]["frt"])

	with open(("../data/"+lset+".bamfrens"), 'w') as filehandle:
	    filehandle.writelines("%s\n" % source for source in sources)
	with open(("../data/"+lset+".bamfrent"), 'w') as filehandle:
	    filehandle.writelines("%s\n" % target for target in targets)
	







