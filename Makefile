MAKE=make

include Makefile_base.mk
include $(EC_ARCH)/Makefile.inc.mk

BASEDIR=$(PWD)

COMPONENTS = utils

COMM     =
OTHERS   =  $(RPNCOMM) lapack blas massvp4 bindcpu_002 $(LLAPI) $(IBM_LD)
#LIBS     = $(MODEL) $(V4D) $(PHY) $(PATCH) $(CHM) $(CPL) $(OTHERS)
LIBS     = $(OTHERS)

DOCTESTPYMODULES = rpn_helpers.py rpnstd.py 

PYVERSIONFILE = rpn_version.py
CVERSIONFILE = rpn_version.h
VERSION   = 1.3.0
LASTUPDATE= 2013-08

versionfile:
	echo "__VERSION__ = '$(VERSION)'" > $(PYVERSIONFILE)
	echo "__LASTUPDATE__ = '$(LASTUPDATE)'" >> $(PYVERSIONFILE)
	echo "#define VERSION \"$(VERSION)\"" > $(CVERSIONFILE)
	echo "#define LASTUPDATE \"$(LASTUPDATE)\"" >> $(CVERSIONFILE)

default: all

# slib: all
# 	r.build \
# 	  -obj $(FTNALLOBJ) \
# 	  -shared \
# 	  -librmn $(RMNLIBSHARED) \
# 	  -o jim.so

all: versionfile
	for i in $(COMPONENTS); \
	do cd $$i ; $(MAKE) all ; cd .. ;\
	done ;\
	python setup.py build

clean:
	rm -f testfile.fst;\
	rm -rf build; \
	for i in $(COMPONENTS); \
	do \
	cd $$i ; $(MAKE) clean0 ; make clean; cd .. ;\
	done

ctags: clean
	rm -f tags TAGS
	for mydir in . $(COMPONENTS); do \
	echo $$mydir ;\
	list2="$$mydir/*.f $$mydir/*.ftn* $$mydir/*.hf"; \
	for myfile in $$list2; do \
		echo $$myfile ;\
		etags --language=fortran --defines --append $$myfile ; \
		ctags --language=fortran --defines --append $$myfile ; \
	done ; \
	list3="$$mydir/*.c $$mydir/*.h"; \
	for myfile in $$list3; do \
		echo $$myfile ;\
		etags --language=c --defines --append $$myfile ; \
		ctags --language=c --defines --append $$myfile ; \
	done ; \
	list4="$$mydir/*.py"; \
	for myfile in $$list4; do \
		echo $$myfile ;\
		etags --language=python --defines --append $$myfile ; \
		ctags --language=python --defines --append $$myfile ; \
	done ; \
	done

alltests: #all
	export PYTHONPATH=$(PWD)/build/lib.$(PYARCH):$(PYTHONPATH) ; \
	echo -e "\n======= PY-DocTest List ========\n" ; \
	for i in $(DOCTESTPYMODULES); \
	do echo -e "\n==== PY-DocTest: " $$i "====\n"; python $$i ;\
	done
	echo -e "\n======= PY-UnitTest List ========\n" ; \
	for i in $(COMPONENTS); \
	do echo -e "\n==== Make Test: " $$i "====\n PYTHONPATH="$(PWD)/build/lib.$(PYARCH):$(PYTHONPATH) "\n"; cd $$i ; $(MAKE) test PYTHONPATH=$(PWD)/build/lib.$(PYARCH):$(PYTHONPATH); cd .. ;\
	done; \
	echo -e "\n======= Other Tests ========\n" ; \
	cd test ; $(MAKE) test PYTHONPATH=$(PWD)/build/lib.$(PYARCH):$(PYTHONPATH); cd ..
