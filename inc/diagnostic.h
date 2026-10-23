/*
 * =====================================================================================
 *
 *       Filename:  diagnostic.h
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  29/01/26 07:24:58
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOUR NAME (), 
 *   Organization:  
 *
 * =====================================================================================
 */

#ifndef DIAGNOSTIC_H  // Check if MY_HEADER_H is not defined
#define DIAGNOSTIC_H  // Define MY_HEADER_H
 
#include "utils.h"


double kling_gupta(const unsigned int n, const double *obs, const double *sim);
double nash_sutcliffe(const unsigned int n, const double *obs, const double *sim);
double log_nash_sutcliffe(const unsigned int n, const double *obs, const double *sim);
double root_mean_squared_error(const unsigned int n, const double *obs, const double *sim);
double perc_bias(const unsigned int n, const double *obs, const double *sim);
double ave_abs_error(const unsigned int n, const double *obs, const double *sim);
double max_abs_error(const unsigned int n, const double *obs, const double *sim);
double peak_diff(const unsigned int n, const double *obs, const double *sim);
double corr_of_error(const unsigned int n, const double *obs, const double *sim);
int numb_of_sign_ch(const unsigned int n, const double *obs, const double *sim);

#endif // End of include guard
