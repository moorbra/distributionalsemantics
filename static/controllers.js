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

       $scope.createModel = function() {
            spinnerService.show('createModelSpinner');
            $scope.showCorpus = false;

            //         .finally(function () {
            // spinnerService.hide('topicsSpinner');
        //});
       };
    });
}());