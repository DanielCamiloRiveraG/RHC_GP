#!/bin/bash

# To run 'run.sh' you must execute './run.sh [test_case] [yes/no]' (e.g './run.sh test_gr4j yes'). The option [yes/no] is to run model using 'valgrind' to check memory leaks.

echo ""
echo "Excecuting $0 for $1"
echo ""

# INPUT DATA 
COMP=true # 'true' or 'false'
EXEC=true # 'true' or 'false'
PLOT=true # 'true' or 'false'
tar_dir=bin # Target dir


testcase=$1 # Test case
orig_dir=$(pwd) # Save the current directory
valgrind=$2 # Valgrind

# GET MODEL NAME
cd "$testcase" || exit 1 # Change to the target directory 
mod_name=$(awk 'NR==13 {print $1}' ctrl.in) # Model name
case "$mod_name" in
    gr4j)
        mod_number=1
        ;;
    hbv)
        mod_number=2
        ;;
    hymod)
        mod_number=3
        ;;
    *)
        echo "Unknown option"
        ;;
esac
cd "$orig_dir" || exit 1 # Return to original directory

# ----- COMPILATION
if $COMP; then
    
    # Change to the target directory 
    cd "$tar_dir" || exit 1
    
    # Change model name within makefile
    sed -i "s/^MODEL =.*/MODEL = $mod_number/" makefile

    # Either using CFLAGS for valgrind or not
    if [ "$valgrind" = "yes" ]; then
        sed -i "s|^CFLAGS =.*|CFLAGS = -I../inc -Wall -Wextra -g -O0|" makefile
    else
        sed -i "s|^CFLAGS =.*|CFLAGS = -I../inc -Wall -Wextra|" makefile
    fi
    
    # Clean up prev compilation
    make clean
    
    # New compilation
    make
fi

# ----- EXECUTION
if $EXEC; then
    # Return to original directory
    cd "$orig_dir" || exit 1
    
    # Either execute the code checking memory with valgrind or not
    if [ "$valgrind" = "yes" ]; then
        valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes ./thym_$mod_name $testcase
    else
        ./thym_$mod_name $testcase
    fi
fi

# ----- PLOTTING
if $PLOT; then
    # Change to tool dir
    cd "./tools" || exit 1
    
    # Plot model results
    ./plot_in_out.py ../$testcase
fi

