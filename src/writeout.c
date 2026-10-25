/*
 * =====================================================================================
 *
 *       Filename:  writeout.c
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  02/10/25 21:07:01
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOUR NAME (), 
 *   Organization:  
 *
 * =====================================================================================
 */

#include "writeout.h"

/*
 * Allocate memory for the modstatev (model-state variables) struct
 */
int allocateMemo_modstatev(const unsigned int size, modstatev *mstv, const unsigned int nq){
    #if MODEL == 1 // GR4J
  
        mstv->s = (double *)calloc(size, sizeof(double));
        mstv->r = (double *)calloc(size, sizeof(double));
        mstv->tsnow = (double *)calloc(size, sizeof(double));
        // Check if calloc succeeded
        if (!mstv->s || !mstv->r || !mstv->tsnow) {
            perror("calloc failed");
            free(mstv->s);
            free(mstv->r);
            free(mstv->tsnow);
            return 1;
        }


    #elif MODEL == 2 // HBV
        
        mstv->sowat = (double *)calloc(size, sizeof(double));
        mstv->sdep = (double *)calloc(size, sizeof(double));
        mstv->ldep = (double *)calloc(size, sizeof(double));
        mstv->stw1 = (double *)calloc(size, sizeof(double));
        mstv->stw2 = (double *)calloc(size, sizeof(double));
        // Check if malloc succeeded
        if (!mstv->sowat || !mstv->sdep || !mstv->ldep || !mstv->stw1 || !mstv->stw2) {
            perror("malloc failed");
            free(mstv->sowat);
            free(mstv->sdep);
            free(mstv->ldep);
            free(mstv->stw1);
            free(mstv->stw2);
            return 1;
        }

    #elif MODEL == 3 // HYMOD
    
        mstv->xhuz = (double *)calloc(size, sizeof(double));
        mstv->xcuz = (double *)calloc(size, sizeof(double));
        mstv->xq = calloc(size, sizeof(double*));
        unsigned int i;
        for (i = 0; i < size; i++) {
            mstv->xq[i] = calloc(nq, sizeof(double));
        }
        mstv->xs = (double *)calloc(size, sizeof(double));
        mstv->snow_store = (double *)calloc(size, sizeof(double));
        // Check if malloc succeeded
        if (!mstv->xhuz || !mstv->xcuz || !mstv->xq || !mstv->xs || !mstv->snow_store) {
            perror("malloc failed");
            free(mstv->xhuz);
            free(mstv->xcuz);
            /* free(mstv->xq); */
            for (i = 0; i < size; i++) {
               free( mstv->xq[i] );
            }
            free(mstv->xq);
            free(mstv->xs);
            free(mstv->snow_store);
            return 1;
        }

   
    #else // IAHCRES
    
    
    #endif

    return 0;
}

/*
 * Allocate memory for the modfluxv (model-fluxes variables) struct
 */
int allocateMemo_modfluxv(const unsigned int size, modfluxv *mfxv){
    #if MODEL == 1 // GR4J

        mfxv->pn = (double *)calloc(size, sizeof(double));
        mfxv->ps = (double *)calloc(size, sizeof(double));
        mfxv->pr = (double *)calloc(size, sizeof(double));
        mfxv->en = (double *)calloc(size, sizeof(double));
        mfxv->es = (double *)calloc(size, sizeof(double));
        mfxv->perc = (double *)calloc(size, sizeof(double));
        mfxv->f = (double *)calloc(size, sizeof(double));
        mfxv->qa = (double *)calloc(size, sizeof(double));
        mfxv->qb = (double *)calloc(size, sizeof(double));
        mfxv->qr = (double *)calloc(size, sizeof(double));
        mfxv->qd = (double *)calloc(size, sizeof(double));
        mfxv->q = (double *)calloc(size, sizeof(double));
        mfxv->rainfall = (double *)calloc(size, sizeof(double));
        mfxv->snowfall = (double *)calloc(size, sizeof(double));
        mfxv->sno = (double *)calloc(size, sizeof(double));
        mfxv->snomlt = (double *)calloc(size, sizeof(double));
        mfxv->eres = (double *)calloc(size, sizeof(double));
        // Check if malloc succeeded
        if (!mfxv->pn || !mfxv->ps || !mfxv->pr || !mfxv->en || !mfxv->es || !mfxv->perc || !mfxv->f || !mfxv->qa || !mfxv->qb || !mfxv->qr || !mfxv->qd || !mfxv->q || !mfxv->rainfall || !mfxv->snowfall || !mfxv->sno || !mfxv->snomlt || !mfxv->eres) {
            perror("calloc failed");
            free(mfxv->pn);
            free(mfxv->ps);
            free(mfxv->pr);
            free(mfxv->en);
            free(mfxv->es);
            free(mfxv->perc);
            free(mfxv->f);
            free(mfxv->qa);
            free(mfxv->qb);
            free(mfxv->qr);
            free(mfxv->qd);
            free(mfxv->q);
            free(mfxv->rainfall);
            free(mfxv->snowfall);
            free(mfxv->sno);
            free(mfxv->snomlt);
            free(mfxv->eres);
            return 1;
        }


    #elif MODEL == 2 // HBV
       
        mfxv->qrou = (double *)calloc(size, sizeof(double));
        mfxv->q = (double *)calloc(size, sizeof(double));
        mfxv->acet = (double *)calloc(size, sizeof(double));
        // Check if malloc succeeded
        if (!mfxv->qrou || !mfxv->q || !mfxv->acet) {
            perror("malloc failed");
            free(mfxv->qrou);
            free(mfxv->q);
            free(mfxv->acet);
            return 1;
        }

    #elif MODEL == 3 // HYMOD

        mfxv->efprecip = (double *)calloc(size, sizeof(double));
        mfxv->ae = (double *)calloc(size, sizeof(double));;
        mfxv->ov = (double *)calloc(size, sizeof(double));;
        mfxv->qq = (double *)calloc(size, sizeof(double));;
        mfxv->qs = (double *)calloc(size, sizeof(double));;
        mfxv->q = (double *)calloc(size, sizeof(double));;
        mfxv->snow = (double *)calloc(size, sizeof(double));;
        mfxv->melt = (double *)calloc(size, sizeof(double));;
        mfxv->pe = (double *)calloc(size, sizeof(double));;
        // Check if calloc succeeded
        if (!mfxv->efprecip || !mfxv->ae || !mfxv->ov || !mfxv->qq || !mfxv->qs || !mfxv->q || !mfxv->snow || !mfxv->melt || !mfxv->pe) {
            perror("malloc failed");
            free(mfxv->efprecip);
            free(mfxv->ae);
            free(mfxv->ov);
            free(mfxv->qq);
            free(mfxv->qs);
            free(mfxv->q);
            free(mfxv->snow);
            free(mfxv->melt);
            free(mfxv->pe);
            return 1;
        }

    
    #else // IAHCRES
    
    #endif

    return 0;
}


/*
 * Free memory for the modstatev (model-state variables) struct
 */
void freeMemo_modstatev(const unsigned int size, modstatev *mstv){
    #if MODEL == 1 // GR4J
    
        free(mstv->s);
        free(mstv->r);
        free(mstv->tsnow);

    #elif MODEL == 2 // HBV
 
        free(mstv->sowat);
        free(mstv->sdep);
        free(mstv->ldep);
        free(mstv->stw1);
        free(mstv->stw2);

    #elif MODEL == 3 // HYMOD

        free(mstv->xhuz);
        free(mstv->xcuz);
        unsigned int i;
        for (i = 0; i < size; i++) {
           free( mstv->xq[i] );
        }
        free(mstv->xq);
        free(mstv->xs);
        free(mstv->snow_store);
    
    
    #else // IAHCRES
    
    
    #endif
}

/*
 * Free memory for the modfluxv (model-fluxes variables) struct
 */
void freeMemo_modfluxv(modfluxv *mfxv){
    #if MODEL == 1 // GR4J

        free(mfxv->pn);
        free(mfxv->ps);
        free(mfxv->pr);
        free(mfxv->en);
        free(mfxv->es);
        free(mfxv->perc);
        free(mfxv->f);
        free(mfxv->qa);
        free(mfxv->qb);
        free(mfxv->qr);
        free(mfxv->qd);
        free(mfxv->q);
        free(mfxv->rainfall);
        free(mfxv->snowfall);
        free(mfxv->sno);
        free(mfxv->snomlt);
        free(mfxv->eres);
    
    #elif MODEL == 2 // HBV
 
        free(mfxv->qrou);
        free(mfxv->q);
        free(mfxv->acet);

    #elif MODEL == 3 // HYMOD
        
        free(mfxv->efprecip); 
        free(mfxv->ae); 
        free(mfxv->ov); 
        free(mfxv->qq); 
        free(mfxv->qs); 
        free(mfxv->q); 
        free(mfxv->snow); 
        free(mfxv->melt); 
        free(mfxv->pe);
    
    #else // IAHCRES
    
    
    #endif
}

/*
 * Write out state and flux variables in 'results.out' file.
 */
void save_model_results(char *filename, const unsigned int n, struct tm *timestamp, const modstatev *mstv, const modfluxv *mfxv, const double *et, const double area){

    FILE *fp = fopen(filename, "w");
    if (fp == NULL) {
        perror("Error opening file");
        return;
    }

    // Conversion constant: k = 1 / (1000 * 86400)
    const double k = 1.0 / 86400000.0;

    // Write header (Se agrega ',q_m3s' al final)

    #if MODEL == 1 // GR4J

            fprintf(fp, "datetime,rainfall_mm,snowfall_mm,sno_mm,tsnow_oC,snomlt_mm,eres_mm,pn_mm,ps_mm,pr_mm,en_mm,es_mm,s_mm,r_mm,perc_mm,f_mm,qa_mm,qb_mm,qr_mm,qd_mm,q_mm,et_mm,q_m3s\n");

    #elif MODEL == 2 // HBV
        fprintf(fp, "datetime,sowat_mm,sdep_mm,ldep_mm,stw1_mm,stw2_mm,acet_mm,q_mm,et_mm,q_m3s\n");

    #elif MODEL == 3 // HYMOD
        fprintf(fp, "datetime,xhuz_mm,snow_store_mm,ae_mm,ov_mm,qq_mm,qs_mm,snow_mm,melt_mm,pe_mm,q_mm,et_mm,q_m3s\n");
    
    #endif

    unsigned int i;
    char buffer[30];
    for (i = 0; i < n; i++) {
        timestamp[i].tm_year -= 1900;
        timestamp[i].tm_mon -= 1;
        strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", &timestamp[i]);

        // q_m3s: (mm/d) * (1 m / 1000 mm) * (1 d / 86400 s) * area (m²)
        double q_m3s = mfxv->q[i] * k * area;

        #if MODEL == 1 // GR4J
                       
                fprintf(fp, "%s,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf\n", buffer, mfxv->rainfall[i], mfxv->snowfall[i], mfxv->sno[i], mstv->tsnow[i], mfxv->snomlt[i], mfxv->eres[i], mfxv->pn[i], mfxv->ps[i], mfxv->pr[i], mfxv->en[i], mfxv->es[i], mstv->s[i], mstv->r[i], mfxv->perc[i], mfxv->f[i], mfxv->qa[i], mfxv->qb[i], mfxv->qr[i], mfxv->qd[i], mfxv->q[i], et[i], q_m3s);

        #elif MODEL == 2 // HBV
   
            fprintf(fp,"%s,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf\n",buffer, mstv->sowat[i], mstv->sdep[i], mstv->ldep[i], mstv->stw1[i], mstv->stw2[i], mfxv->acet[i], mfxv->q[i], et[i], q_m3s);
        
        #elif MODEL == 3 // HYMOD
        
            fprintf(fp,"%s,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf,%.8lf\n",buffer, mstv->xhuz[i], mstv->snow_store[i], mfxv->ae[i], mfxv->ov[i], mfxv->qq[i], mfxv->qs[i], mfxv->snow[i], mfxv->melt[i], mfxv->pe[i], mfxv->q[i], et[i], q_m3s);
        
        #else // IAHCRES
        
        
        #endif

    }

    fclose(fp);
    /* printf("Time series written to %s\n", filename); */

}

/*
 * Write out diagnostic metrics in 'diagnostic.out' file.
 */
void save_model_diagnostic(char *filename, const unsigned int n, const double *obs, const double *sim){

    FILE *fp = fopen(filename, "w");
    if (fp == NULL) {
        perror("Error opening file");
        return;
    }

    fprintf(fp,"KGE,%0.8lf\n",   kling_gupta( n, obs, sim));
    fprintf(fp,"NSE,%0.8lf\n", nash_sutcliffe(  n,   obs,   sim));
    fprintf(fp,"LNSE,%0.8lf\n",  log_nash_sutcliffe( n,   obs,   sim));
    fprintf(fp,"RMSE,%0.8lf\n",  root_mean_squared_error( n,   obs,   sim));
    fprintf(fp,"PBIAS,%0.8lf\n",  perc_bias( n,   obs,   sim));
    fprintf(fp,"ABSER,%0.8lf\n",  ave_abs_error( n,   obs,   sim));
    fprintf(fp,"ABSMAXER,%0.8lf\n",  max_abs_error( n,   obs,   sim));
    fprintf(fp,"PDIFF,%0.8lf\n",  peak_diff( n,   obs,   sim));
    fprintf(fp,"ERCOR,%0.8lf\n",  corr_of_error( n,   obs,   sim));
    fprintf(fp,"NSC,%d", numb_of_sign_ch( n,   obs,   sim));

    fclose(fp);

}

