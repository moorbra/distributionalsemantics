(function() {
    var app = angular.module('semantics', ['ui.bootstrap', 'angularUtils.directives.dirPagination', 'ngFlash', 'angularSpinners']);

    app.controller('wikipediaController', function($scope, $http, Flash, spinnerService) {
       $scope.categoryFilter = "";
       $scope.categories = [];
       $scope.categoriesPerPage = 10;
       $scope.documentsPerPage = 10;
       $scope.documents = [];
       $scope.selectedCategory = "";
       $scope.showCategories = false;
       $scope.corpus = [];
       $scope.corpDocsPerPage = 10;
       $scope.creatingModel = false;
       $scope.showCorpus = true;
       $scope.logs = []
       $scope.showDocuments = false;

       $scope.getCategories = function() {
           $scope.showDocuments = false;
            resource = $scope.categoryFilter == "" ? "wikipedia/categories" : "wikipedia/categories/" + $scope.categoryFilter;
            $scope.categoryFilter = $scope.categoryFilter == "" ? "a" : $scope.categoryFilter
            $http.get(resource)
            .then(function(data, status, header, config) {
                $scope.categories = data.data;
                $scope.showCategories = true;
            });
       };

       $scope.getDocuments = function(category) {
            $http.get("wikipedia/documentlist/" + category)
            .then(function(data, status, header, config) {
                $scope.selectedCategory = category;                
                $scope.documents = data.data.categorymembers;
                $scope.showDocuments = true;
            });
       };

       $scope.addDocument = function(documentTitle, category) {
            var document = $scope.corpus.find(doc => doc.title === documentTitle);
            if(document === undefined) {
                $scope.corpus.push({
                    title: documentTitle,
                    category: category
                });
                Flash.create('success', "Document '" + documentTitle + "' added to corpus.");                                            
                return;
            }           
            Flash.create('warning', "Document '" + documentTitle + "' already exists in corpus.");
       };

       $scope.removeDocument = function(documentTitle) {
            $scope.corpus = $scope.corpus.filter(function(el) { return el.title != documentTitle; });
       };

       $scope.createModel = function(wikimodelname) {
            spinnerService.show('createModelSpinner');
            $scope.showCorpus = false;
            $scope.logs = [];
            $scope.logs.push("Downloading documents from Wikipedia.");
            $http.post('wikipedia/documentlist', {'documents' : $scope.corpus, 'modelName': wikimodelname})
            .then(function (data, status, headers, config) {
                corpusManifest = data.data;
                $scope.logs.push("Downloaded " + corpusManifest.downloadedDocuments + " from Wikipedia.");
                $scope.logs.push("Creating distributional semantic model.");
                $http.post('modeller/createmodel', {'corpusPath' : corpusManifest.corpusPath, 'modelname': wikimodelname})
                .then(function (data, status, headers, config) {
                    modelManifest = data.data
                    $scope.logs.push("Created model with " + modelManifest.numberterms + " terms.");
                })
            })
            .finally(function() {
                spinnerService.hide('createModelSpinner');
                $scope.showCorpus = true;
            });
       };
    });

    app.controller('modelsController', function($scope, $http, Flash, spinnerService) {
        $scope.models = [];
        $scope.modelsPerPage = 10;
        $scope.selectedModel = null;
        $scope.termsPerPage = 10;
        $scope.similarterms = null;
        $scope.terma = "";
        $scope.termb = "";
        $scope.direction = "";
        $scope.calculatedSimularities = null;
        $scope.showmodeldetails = false;
        $scope.showTermSimilarity = false;
        $scope.showCalculationSimilarity = false;

        $scope.getModels = function () {
            $http.get('manifest/manifests')
            .then(function (data, status, headers, config) {
                $scope.models = data.data;
            });
        };

        $scope.getModelDetails = function(modelname) {            
            $http.get('manifest/manifests/' + modelname)
            .then(function (data, status, headers, config) {
                $scope.selectedModel = data.data;
                $scope.showmodeldetails = true;
                $scope.showTermSimilarity = false;
                $scope.showCalculationSimilarity = false;                
            });
        };

        $scope.getTermSimilarities = function(term, direction) {
            $http.get('similarity/' + $scope.selectedModel.modelname + '/'+ term + '/' + direction)
            .then(function (data, status, headers, config) {
                $scope.similarterms = data.data;
                $scope.showTermSimilarity = true;                        
            });            
        };

        $scope.deleteModel = function(modelname) {
            $scope.selectedModel = null;
            $scope.showmodeldetails = false;
            $scope.showTermSimilarity = false;
            $scope.showCalculationSimilarity = false;             
            $http.delete('modeller/' + modelname)
            .then(function (data, status, headers, config) {
                $scope.getModels();
            });            
        };

        $scope.calculateTermSimilarites = function(terma, termb, direction) {
            $http.post('similarity/compareterms', {'modelname': $scope.selectedModel.modelname, 'terms': [terma, termb], 'direction': direction})
            .then(function (data, status, headers, config) {
                $scope.calculatedSimularities = data.data;
                $scope.showCalculationSimilarity = true;
            });
        };

        $scope.getModels();
    });
}());