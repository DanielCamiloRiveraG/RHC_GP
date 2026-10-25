#include <stdio.h>
#include <stdlib.h>

#include "utils.h"
#include "snow.h"
#include "readin.h"
#include "writeout.h"
#include "evapotrans.h"
#include "model.h"


int main(int argc, char **argv){

    if (argc < 2) {
        printf("Usage: %s <arguments>\n", argv[0]);
        return 1;
    }

    //--------- Print banner with basic information
    print_box_banner("Tropical Hydrological Modeling (THYM)", "Author: Luis Morales-Marin", "Universidad Nacional de Colombia");

    //--------- Read test-case name
    ininfo ininf;
    read_init(argv[1], &ininf);
    /* printf("%s\n", ininf.meteoinf); */

    //--------- Read ctrl.in file
    ctrlbasic ctrlb;
    /* ctrlout ctrlo; */
    modparam modp;
    evapot evp;
    read_ctrl(ininf.ctrlinf, &ctrlb, &modp, &evp);

    //--------- Read meteo.in file
    // Get the time interval to read in meteo.in input file
    meteoini metini;
    get_time_interval_meteo_in(ininf.meteoinf, ctrlb.startdt, ctrlb.enddt, &metini);
    printf("sdt: %d, edt: %d, ntimes: %d \n", metini.sdt, metini.edt, metini.ntimes); 
    meteoin metin;

    allocateMemo(metini.ntimes, &metin);
   
    struct tm *dts = (struct tm *)malloc(metini.ntimes * sizeof(struct tm));
    // Check if malloc succeeded
    if (dts == NULL) {
        printf("Memory allocation failed!\n");
        return 1;
    }
    //struct tm dts[nlines];
    //read_meteo("../test/meteo.in");
    evp.et = (double *)malloc(metini.ntimes * sizeof(double));
    // Check if malloc succeeded
    if (evp.et == NULL) {
        printf("Memory allocation failed!\n");
        return 1;
    }

    read_meteo(ininf.meteoinf, &metin, &metini, dts, evp.et);
    printf("year: %d, month: %d, day: %d, jday: %d, et: %f, runoff: %f\n", metin.timestamp[0].tm_year, metin.timestamp[0].tm_mon, metin.timestamp[0].tm_mday, metin.timestamp[0].tm_yday+1, evp.et[0], metin.runoff[0]);
    printf("year: %d, month: %d, day: %d, jday: %d, et: %f\n", metin.timestamp[metini.ntimes-1].tm_year, metin.timestamp[metini.ntimes-1].tm_mon,metin.timestamp[metini.ntimes-1].tm_mday, metin.timestamp[metini.ntimes-1].tm_yday+1, evp.et[metini.ntimes-1]);

    
    //--------- Compute evapotranspiration
    ets(evp.etmethod, metin.tmin, metin.tave, metin.tmax, metin.windv, metin.timestamp, ctrlb.lat, metini.ntimes, ctrlb.alt, evp.albedo, evp.u_alt, evp.et);

    //--------- Simulate using a conceptual rainfall-runoff model
   	printf("\n");
	printf("******* RUNNING '%s' FOR TESTCASE '%s' *******\n",modp.model, argv[1]);
	printf("\n");

    modstatev mstv;
    allocateMemo_modstatev(metini.ntimes, &mstv, modp.nq);
    modfluxv mfxv;
    allocateMemo_modfluxv(metini.ntimes, &mfxv);
    #if MODEL == 1 // GR4J
       gr4j(metini.ntimes, metin.tave, metin.precip, metin.tmax, evp.et, &modp, &mstv, &mfxv, metin.timestamp);

    #elif MODEL == 2 // HBV
       hbv(metini.ntimes, metin.tave, metin.precip, evp.et, &modp, &mstv, &mfxv);
    
    
    #elif MODEL == 3 // HYMOD
       hymod(metini.ntimes, metin.tave, metin.precip,  evp.et, &modp, &mstv, &mfxv);
    
    #else // IAHCRES
    
    #endif
   
    // Print model output
    save_model_results(ininf.resultsoutf, metini.ntimes, metin.timestamp, &mstv, &mfxv, evp.et, ctrlb.area);

    // Print model diagnostic metrics
    save_model_diagnostic(ininf.diagnosticoutf, metini.ntimes, metin.runoff, mfxv.q);
    

    // Free memory 
    freeininfo(&ininf);  // from ininf
    /* freectrlout(&ctrlo); // from ctrlo  */
    free(dts);           // from tm structure
    free(evp.et);           // 
    freememo(metin.timestamp, metin.tave, metin.tmin, metin.tmax, metin.precip, metin.windv, metin.runoff);
    freeMemo_modstatev(metini.ntimes, &mstv);
    freeMemo_modfluxv(&mfxv);
    
    return 0;
}

