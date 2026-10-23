/*
 * =====================================================================================
 *       Filename:  diagnostic.c
 *    Description:  Hidrological diagnostic functions (Corrected to Standard)
 * =====================================================================================
 */

#include "diagnostic.h"

/*
 * Kling-Gupta Efficiency Modificado (KGE' - Kling et al., 2012)
 * Desacopla la variabilidad (gamma) del sesgo de volumen (beta)
 * usando la relación de coeficientes de variación (CV_sim / CV_obs).
 */
double kling_gupta(const unsigned int n, const double *obs, const double *sim){

    if (n <= 1) return 0.0;

    // 1. Promedios
    double obs_sum = 0.0;
    double sim_sum = 0.0;
    unsigned int i;
    for(i = 0; i < n; i++){
        obs_sum += obs[i];
        sim_sum += sim[i];
    }
    double obs_mean = obs_sum / (double)n;
    double sim_mean = sim_sum / (double)n;

    // 2. Varianzas y Covarianza
    double sum_obs_sq = 0.0;
    double sum_sim_sq = 0.0;
    double sum_cov = 0.0;

    for(i = 0; i < n; i++){
        double d_obs = obs[i] - obs_mean;
        double d_sim = sim[i] - sim_mean;
        sum_obs_sq += d_obs * d_obs;
        sum_sim_sq += d_sim * d_sim;
        sum_cov    += d_obs * d_sim;
    }

    double obs_std = sqrt(sum_obs_sq / (double)n);
    double sim_std = sqrt(sum_sim_sq / (double)n);

    // Protecciones contra división por cero
    if (obs_std == 0.0 || obs_mean == 0.0 || sim_mean == 0.0) {
        return 0.0;
    }

    // 3. Correlación de Pearson (r)
    double r = 0.0;
    if (sum_obs_sq > 0.0 && sum_sim_sq > 0.0) {
        r = sum_cov / (sqrt(sum_obs_sq) * sqrt(sum_sim_sq));
    }

    // 4. Componentes KGE Modificado (2012)
    double alpha = sim_std / obs_std;
    double beta  = sim_mean / obs_mean;
    double gamma = alpha / beta;  // Gamma sustituye a Alpha (CV_sim / CV_obs)

    // 5. Cálculo final de KGE' (2012)
    double term_r = (r - 1.0) * (r - 1.0);
    double term_g = (gamma - 1.0) * (gamma - 1.0);
    double term_b = (beta - 1.0) * (beta - 1.0);

    return 1.0 - sqrt(term_r + term_g + term_b);
}

/*
 * Nash-Sutcliffe efficiency (NSE)
 * Fórmula estándar correcta
 */
double nash_sutcliffe(const unsigned int n, const double *obs, const double *sim){

    double obs_mean = mean_double(n, obs);

    unsigned int i;
    double num = 0.0;
    double den = 0.0;
    for(i = 0; i < n; i++){
       num += (sim[i] - obs[i]) * (sim[i] - obs[i]);
       den += (obs_mean - obs[i]) * (obs_mean - obs[i]);
    }

    if (den != 0.0) {
        return 1.0 - (num / den);
    } else {
        return 0.0;
    }
}


/*
 * Log Nash-Sutcliffe efficiency (LNSE)
 * CORREGIDO: Calcula el promedio de log(obs) en lugar del logaritmo del promedio.
 * Incluye protección (eps) para evitar log(0) o valores negativos.
 */
double log_nash_sutcliffe(const unsigned int n, const double *obs, const double *sim){

    double eps = 1e-6; // Valor pequeño para evitar log(0)
    double log_obs_sum = 0.0;
    unsigned int i;

    // 1. Calcular el promedio de los logaritmos de las observaciones
    for(i = 0; i < n; i++){
        double o = (obs[i] <= 0.0) ? eps : obs[i];
        log_obs_sum += log(o);
    }
    double log_obs_mean = log_obs_sum / (double)n;

    // 2. Calcular numerador y denominador
    double num = 0.0;
    double den = 0.0;
    for(i = 0; i < n; i++){
        double o = (obs[i] <= 0.0) ? eps : obs[i];
        double s = (sim[i] <= 0.0) ? eps : sim[i];
        
        num += (log(s) - log(o)) * (log(s) - log(o));
        den += (log_obs_mean - log(o)) * (log_obs_mean - log(o));
    }

    if (den != 0.0) {
        return 1.0 - (num / den);
    } else {
        return 0.0;
    }
}


/*
 * Root-mean-squared error (RMSE)
 * CORREGIDO: Se añade la división entre 'n' dentro de la raíz cuadrada.
 */
double root_mean_squared_error(const unsigned int n, const double *obs, const double *sim){

    unsigned int i;
    double sum = 0.0;
    for(i = 0; i < n; i++){
       sum += (sim[i] - obs[i]) * (sim[i] - obs[i]);
    }

    if (sum >= 0.0 && n > 0) {
        return sqrt(sum / (double)n);
    } else {
        printf("Cannot take sqrt of negative number\n");
        return 0.0;
    }
}


/*
 * Percentage bias (PBIAS)
 * CORREGIDO: Se multiplica por 100 para obtener el porcentaje real (%).
 */
double perc_bias(const unsigned int n, const double *obs, const double *sim){

    unsigned int i;
    double num = 0.0;
    double den = 0.0;
    for(i = 0; i < n; i++){
       num += sim[i] - obs[i]; 
       den += obs[i];
    }

    if (den != 0.0) {
        return 100.0 * (num / den);
    } else {
        return 0.0;
    }
}


/*
 * Average absolute error
 */
double ave_abs_error(const unsigned int n, const double *obs, const double *sim){

    unsigned int i;
    double sum = 0.0;
    for(i = 0; i < n; i++){
       sum += fabs(sim[i] - obs[i]); 
    }

    return sum / (double)n;
}


/*
 * Maximum absolute error
 */
double max_abs_error(const unsigned int n, const double *obs, const double *sim){

    unsigned int i = 0;
    double dummy;
    double maxv = fabs(sim[0] - obs[0]);
    for(i = 1; i < n; i++){
        dummy = fabs(sim[i] - obs[i]);
        if (maxv < dummy) {
            maxv = dummy;
        }
    }
    return maxv;
}


/*
 * Peak difference
 */
double peak_diff(const unsigned int n, const double *obs, const double *sim){

    unsigned int i = 0;
    double max_sim = sim[0];
    for(i = 1; i < n; i++){
        if (max_sim < sim[i]) {
            max_sim = sim[i];
        }
    }

    double max_obs = obs[0];
    for(i = 1; i < n; i++){
        if (max_obs < obs[i]) {
            max_obs = obs[i];
        }
    }
    
    return max_sim - max_obs;
}


/*
 * Correlation of error
 */
double corr_of_error(const unsigned int n, const double *obs, const double *sim){

    double obs_stddev = stddev_double(n, obs);
    double sim_stddev = stddev_double(n, sim);

    if (obs_stddev * sim_stddev == 0.0 || n <= 1) {
        return 0.0;
    }

    unsigned int i;
    double sum = 0.0;
    for(i = 0; i < n - 1; i++){
       sum += (sim[i] - obs[i]) * (sim[i+1] - obs[i+1]);
    }

    return (1.0 / (obs_stddev * sim_stddev)) * (1.0 / (double)(n - 1)) * sum;
}


/*
 * Number of sign changes
 */
int numb_of_sign_ch(const unsigned int n, const double *obs, const double *sim){

    unsigned int i = 0;
    double diff1 = sim[i] - obs[i];
    double diff2;
    int nchanges = 0;
    for(i = 1; i < n; i++){
        diff2 = sim[i] - obs[i];
        if ( (diff1 > 0 && diff2 < 0) || (diff1 < 0 && diff2 > 0) ){
            nchanges += 1;
        } else if ( (diff1 == 0 && diff2 < 0) || (diff1 == 0 && diff2 > 0) ){
            nchanges += 1;
        } else if ( (diff1 > 0 && diff2 == 0) || (diff1 < 0 && diff2 == 0) ){
            nchanges += 1;
        }
        diff1 = diff2;
    }

    return nchanges;
}
