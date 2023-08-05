/* Generates the splines according to the splineTypes and number of points */
vector<Spline> calculateSplines(vector<double> x, vector<double> y, int splineType) {

    vector<Spline> splines;

    vector<int> numberOfAbscissaeSeparatingConsecutiveKnots_vector = {0, 2, 5};

    if (splineType == 1 || x.size() < 3)  // if model or len(x) < 3 --> just one spline
        splines = vector<Spline>(1);
    else if (x.size() < 5)
        splines = vector<Spline>(2);
    else
        splines = vector<Spline>(3);

    for (int i = 0; i < splines.size(); i++) {
        splines[i].solve(x, y, splineType, numberOfAbscissaeSeparatingConsecutiveKnots_vector[i]);
        if (removeAsymptotes == true){
            splines[i].removeAsymptotes();
        }
        splines[i].normalizeCoefficients(
                                        -splines[i].yD0Min,
                                        splines[i].yD0Max - splines[i].yD0Min,
                                        splines[i].yD1MaxAbs);
    }

    return splines;

}

double summedSquaredError(vector <double> b, vector<double> c){
    double SSE = 0;
    for(int i=0; i < b.size(); i++){
        SSE += pow((b[i] - c[i]), 2);
    }
    return SSE;
}

vector<double> logLikeliHood(double n, vector<double> residuals){

    vector<double> ll;

    for(int i=0; i < residuals.size(); i++)
        ll.push_back(n * log(residuals[i] / n));

    return ll;

}

vector<vector<double>> informationCriterion(vector<double> ll, int n, vector<int> numOfParam){

    vector<vector<double>> information ;
    vector<double> AIC;
    vector<double> correctionAIC;
    vector<double> AICc;
    vector<double> BIC;
    vector<double> k;

    for(int i=0;i<numOfParam.size();i++)
        k.push_back(2*(numOfParam[i]+1)+1);

    for(int i=0; i<ll.size();i++){

        AIC.push_back(2*k[i]+ll[i]);
        correctionAIC.push_back(2*k[i]*(k[i]+1)/(n-k[i]-1));
        BIC.push_back(ll[i]+k[i]*log(n));
    }
    for (int i = 0; i<correctionAIC.size(); i++)
        AICc.push_back(AIC[i]+correctionAIC[i]);

    information.push_back(AIC);
    information.push_back(AICc);
    information.push_back(BIC);
    information.push_back(k);

    return information;

}

/* Return the index of the minimum element */
int positionOfMinimum(vector<double> v){
    return min_element(v.begin(), v.end()) - v.begin();
}

/* Given a vector of Splines return the best spline based on the criterion */
int calculateBestSpline(vector<Spline> splines, string criterion){

    // If the length of splines is 1 then the only spline is the best spline
    if (splines.size() == 1){
        return 0;
    }

    vector<int> numOfParam;
    vector<double> AIC;
    vector<double> AICc;
    vector<double> BIC;
    vector<double> AICplusAICc;
    vector<double> SSE;
    vector<double> ll;
    vector<vector<double>> information;
    vector<double> ratioLK;
    vector<double> k;
    // The original X vector is in every Spline. I take it from the first one
    int numOfObs = splines[0].originalAbscissae.size();

    int indexBestSpline;

    for (int k=0; k < splines.size(); k++){
        vector<double> ySpl_tmp;
        for (int i=0; i < numOfObs;i++){
            ySpl_tmp.push_back(splines[k].D0(splines[0].originalAbscissae[i]));
        }
        SSE.push_back(summedSquaredError(splines[0].originalOrdinates, ySpl_tmp));
    }

    ll = logLikeliHood(numOfObs,SSE);

    for(int i=0;i<splines.size();i++){
        numOfParam.push_back(splines[i].K);
    }

    information = informationCriterion(ll, numOfObs, numOfParam);

    AIC = information[0];
    AICc = information[1];
    BIC = information[2];
    k = information[3];


    if (criterion == "SSE"){
        indexBestSpline = positionOfMinimum(SSE);
    }

    if (criterion == "AIC"){
        for (int i=0; i<k.size();i++){
            ratioLK.push_back(k[i] / numOfObs);
        }
        for (int i=0; i < ratioLK.size(); i++){
            if (ratioLK[i] <= numberOfRatiolkForAICcUse){
                AICplusAICc.push_back(AICc[i]);
            }
            else{
                AICplusAICc.push_back(AIC[i]);
            }
        }
        indexBestSpline = positionOfMinimum(AICplusAICc);
    }


    if (criterion == "BIC"){
        indexBestSpline = positionOfMinimum(BIC);
    }

    return indexBestSpline;
}
