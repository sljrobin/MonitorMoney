# MoniMoney: Makefile

MM=@clear; python3 monimoney.py
# Accounts: Great Britain
GB_ACCOUNT="./data/statements/gb/hsbc/account.json"

# Fonctions
define analysis
	$(MM) analysis --start=$(1) --end=$(2) $(3)
endef

define statement
	$(MM) statement --start=$(1) --end=$(2) $(3)
endef

# Rules files
include ./data/rules/2019.mk
include ./data/rules/2020.mk

# Rules
# Rule: check GBP rate
check:
	@python3 ./data/rules/check-gbp.py $(alert)
# Rule: convert GBP to EUR
convert:
	@python3 ./data/rules/convert-gbp.py
# Rule: create a new transaction
create:
	$(MM) create
# Rule: edit statement files
edit:
	@vim -c 'execute "norm /transactions\n"' -p $(GB_ACCOUNT)
# Rule: generate a Makefile rule
generate:
	$(MM) generate --rule=$(month)
# Rule: generate a graph
graph:
	@termgraph ./data/graphs/graph-example.dat --width 20
# Rule: run the last analysis
last:
	$(MAKE) 2019-sep_analysis
