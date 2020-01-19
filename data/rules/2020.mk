# 2020: Jan
2020-jan_analysis:
	$(call analysis,2019-12-25,2020-01-24,--statement=$(GB_ACCOUNT))
2020-jan_analysis-all:
	$(call analysis,2019-12-25,2020-01-24,--all)
2020-jan_statement:
	$(call statement,2019-12-25,2020-01-24,--statement=$(GB_ACCOUNT))
2020-jan_statement-all:
	$(call statement,2019-12-25,2020-01-24,--all)
