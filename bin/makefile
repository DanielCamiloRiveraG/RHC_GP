# Define the compiler and the flags
CC = gcc
CFLAGS = -I../inc -Wall -Wextra
LDFLAGS = -lm  # Link math library

# Define the source and header files
SRCDIR = ../src
INCDIR = ../inc
BINDIR = .
BINDIR2 = bin
BASENAME = thym

# Define other varible
MODEL = 3

# Setup rainfall-runoff model name
ifeq ($(MODEL),1)
	MODELNAME=gr4j
else ifeq ($(MODEL),2)
	MODELNAME=hbv
else ifeq ($(MODEL),3)
	MODELNAME=hymod
endif

# List of source files
SOURCES = $(wildcard $(SRCDIR)/*.c)

# Generate object files from source files
OBJECTS = $(SOURCES:$(SRCDIR)/%.c=$(BINDIR)/%.o)

# Name of the output binary
TARGET = $(BINDIR)/$(BASENAME)_$(MODELNAME)

# Rule for building the program
all: $(TARGET) symlink

# Rule for compiling the program
$(TARGET): $(OBJECTS)
	$(CC) -o $@ $^ $(LDFLAGS)

# Rule for compiling the source files into object files
$(BINDIR)/%.o: $(SRCDIR)/%.c
	$(CC) $(CFLAGS) -DMODEL=$(MODEL) -c $< -o $@
	
# Create symbolic link
LINK_NAME = ../$(BASENAME)_$(MODELNAME)
symlink:
	@rm -f $(LINK_NAME)  # Remove the existing link if it exists
	@ln -s $(BINDIR2)/$(BASENAME)_$(MODELNAME) $(LINK_NAME)

# Rule for cleaning up object files and the binary
clean:
	rm -f $(BINDIR)/*.o $(TARGET)

# Phony targets
.PHONY: all clean
CC=gcc

