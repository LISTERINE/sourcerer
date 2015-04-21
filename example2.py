from sourcerer.parser import YAMLProcessor

gen = YAMLProcessor()
gen.load('sample_data/sample.yml')
gen.output()
