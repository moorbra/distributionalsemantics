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

       $scope.getCategories = function() {
            resource = $scope.categoryFilter == "" ? "wikipedia/categories" : "wikipedia/categories/" + $scope.categoryFilter;
            $scope.categoryFilter = $scope.categoryFilter == "" ? "a" : $scope.categoryFilter
            $http.get(resource)
            .then(function(data, status, header, config) {
                $scope.categories = data.data;
            });
       };

       $scope.getDocuments = function(category) {
            $http.get("wikipedia/documentlist/" + category)
            .then(function(data, status, header, config) {
                $scope.selectedCategory = category;                
                $scope.documents = data.data.categorymembers;
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
}());