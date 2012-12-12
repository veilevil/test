'use strict';

/* Controllers */

function TaskListCtrl($scope,$http) {
    $http.get("/todos")
        .success(function(data) {
            $scope.todos=data;
        }).error(function(data) {
            alert("server error");
        });
    $scope.edit=function(todotoedit){
        $http.post("/todo/edit")
            .success(function(data) {
                $scope.todotoedit={};
                for(var b in $scope.todos)
                {
                    if($scope.todos[b]._id==todotoedit._id){
                        $scope.todos[b]=todotoedit;
                    }
                }
            }).error(function(data) {
                alert("server error");
            });
    }
}