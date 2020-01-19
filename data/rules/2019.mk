# 2019: Sep
2019-sep_analysis:
	$(call analysis,2019-08-23,2019-09-24,--statement=$(GB_ACCOUNT))
2019-sep_analysis-all:
	$(call analysis,2019-08-23,2019-09-24,--all)
2019-sep_statement:
	$(call statement,2019-08-23,2019-09-24,--statement=$(GB_ACCOUNT))
2019-sep_statement-all:
	$(call statement,2019-08-23,2019-09-24,--all)

# 2019: Oct
2019-oct_analysis:
	$(call analysis,2019-09-25,2019-10-24,--statement=$(GB_ACCOUNT))
2019-oct_analysis-all:
	$(call analysis,2019-09-25,2019-10-24,--all)
2019-oct_statement:
	$(call statement,2019-09-25,2019-10-24,--statement=$(GB_ACCOUNT))
2019-oct_statement-all:
	$(call statement,2019-09-25,2019-10-24,--all)

# 2019: Nov
2019-nov_analysis:
	$(call analysis,2019-10-25,2019-11-24,--statement=$(GB_ACCOUNT))
2019-nov_analysis-all:
	$(call analysis,2019-10-25,2019-11-24,--all)
2019-nov_statement:
	$(call statement,2019-10-25,2019-11-24,--statement=$(GB_ACCOUNT))
2019-nov_statement-all:
	$(call statement,2019-10-25,2019-11-24,--all)

# 2019: Dec
2019-dec_analysis:
	$(call analysis,2019-11-25,2019-12-24,--statement=$(GB_ACCOUNT))
2019-dec_analysis-all:
	$(call analysis,2019-11-25,2019-12-24,--all)
2019-dec_statement:
	$(call statement,2019-11-25,2019-12-24,--statement=$(GB_ACCOUNT))
2019-dec_statement-all:
	$(call statement,2019-11-25,2019-12-24,--all)
