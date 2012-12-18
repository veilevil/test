'use strict';

/* Controllers */

function TaskListCtrl($scope,$http) {
    $http.get("/todos")
        .success(function(data) {
            $scope.todos=data;
        }).error(function(data) {
            alert("server error");
        });
    $scope.setedit=function(todotoedit){
        $scope.currenttodo = todotoedit;
    };
    $scope.create=function(todotoadd){
        $http.put("/create",todotoadd)
            .success(function(data) {
                $scope.additem={};
                
                $scope.todos.unshift(data);
            }).error(function(data) {
                alert("server error");
            });
    };
    $scope.update=function(todotoedit){
        $http.post("/update",todotoedit)
            .success(function(data) {
                $scope.currenttodo={};
            }).error(function(data) {
                alert("server error");
            });
    };
    $scope.destroy=function(id){
        $http.delete("/destroy/"+id)
            .success(function(data) {
//                $scope.currenttodo={};
                for(var b in $scope.todos)
                {
                    if($scope.todos[b]._id==id){
                        $scope.todos.splice(b,1);
                    }
                }
            }).error(function(data) {
                alert("server error");
            });
    };
}