/*
 * =====================================================================================
 *
 *       Filename:  writeout.h
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  02/10/25 21:08:59
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOUR NAME (), 
 *   Organization:  
 *
 * =====================================================================================
 */

#ifndef WRITEOUT_H  // Check if MY_HEADER_H is not defined
#define WRITEOUT_H  // Define MY_HEADER_H

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#include "snow.h"
#include "diagnostic.h"

/*
 * Defining object types
 */

/* Model state variables (other format) */
typedef struct {

    #if MODEL == 1 // GR4J

        double *s;
        double *r;
        /* Snow modeling state variables */
        double *tsnow;

    #elif MODEL == 2 // HBV
        
        double *sowat;
        double *sdep;
        double *ldep;
        double *stw1;
        double *stw2;

    #elif MODEL == 3 // HYMOD

        double *xhuz;        //Model computed upper zone soil moisture tank state height
        double *xcuz;        //Model computed upper zone soil moisture tank state contents
        double **xq;         //Model computed quickflow tank states contents
        double *xs;          //Model computed slowflow tank state contents
        double *snow_store;      //State of snow reservoir   
    
    #else // IAHCRES
    
    #endif

} modstatev;

/* Model fluxes variables */
typedef struct {

    #if MODEL == 1 // GR4J

        double *pn;
        double *ps;
        double *pr;
        double *en;
        double *es;
        double *perc;
        double *f;
        double *qa;
        double *qb;
        double *qr;
        double *qd;
        double *q;
    
        /* Snow modeling state variables */
        double *rainfall;
        double *snowfall;
        double *sno;
        double *snomlt;
        double *eres;

    #elif MODEL == 2 // HBV
        
       double *qrou; // Maxbas - routing Q's 
       double *q; // array of outflow Q's for simulation
       double *acet; // Actual evapotranspiration

    #elif MODEL == 3 // HYMOD
    
       double *efprecip;   //Effective rain entering the SMA model (melt+precip if using snow model)
       double *ae;          //Model computed actual evapotranspiration flux
       double *ov;          //Model computed precipitation excess flux
       double *qq;          //Model computed quickflow flux
       double *qs;          //Model computed slowflow flux
       double *q;           //Model computed total streamflow flux
       double *snow;        //Daily snow
       double *melt;        //Snow melt
       double *pe;          // Potential ET (Hamon)

    #else // IAHCRES
    
    #endif
} modfluxv;

/*
 * Function prototypes
 */
void save_model_results(char *filename, const unsigned int n, struct tm *timestamp, const modstatev *mstv, const modfluxv *mfxv, const double *et, const double area);
void save_model_diagnostic(char *filename, const unsigned int n, const double *obs, const double *sim);
int allocateMemo_modstatev(const unsigned int size, modstatev *mstv, const unsigned int nq);
void freeMemo_modstatev(const unsigned int size, modstatev *mstv);
int allocateMemo_modfluxv(const unsigned int size, modfluxv *mfxv);
void freeMemo_modfluxv(modfluxv *mfxv);

#endif // End of include guard
