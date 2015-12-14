(function () {
    'use strict';

    angular
        .module('application.tasks.controllers')
        .controller('CurrentTaskController', function (Events, Tasks, $http, $scope, $location, Auth, $window,
                                                       $routeParams, UsersInTask, Subtasks, $timeout) {
            var vm = this;
            vm.isLoggedIn = !!Auth.getToken();

            vm.init = function () {
                vm.today = new Date();
                if ($location.search().taskId) {
                    Tasks.get({
                        eventId: $location.search().eventId,
                        taskId: $location.search().taskId
                    }, function (data) {
                        vm.task = JSON.parse(angular.toJson(data));
                        vm.task.finish_time = new Date(vm.task.finish_time);
                        vm.isTaskHeader = Auth.getUserId() == data.task_header.id;
                        vm.edit = {
                            description: {
                                value: angular.copy(vm.task.description),
                                status: false,
                                changeStatus: function () {
                                    vm.edit.description.status = !vm.edit.description.status;
                                    vm.edit.description.value = angular.copy(vm.task.description);
                                },
                                update: function () {
                                    vm.task.description = vm.edit.description.value;
                                    Tasks.update({
                                        eventId: $location.search().eventId,
                                        taskId: $location.search().taskId
                                    }, {
                                        description: vm.task.description
                                    }, function (response) {
                                        vm.edit.description.status = false;
                                    })
                                }
                            },
                            finish_time: {
                                value: angular.copy(vm.task.finish_time),
                                status: false,
                                changeStatus: function () {
                                    vm.edit.finish_time.status = !vm.edit.finish_time.status;
                                    vm.edit.finish_time.value = angular.copy(vm.task.finish_time);
                                    console.log(vm.today);
                                },
                                update: function () {
                                    console.log(dateFormat(new Date(vm.edit.finish_time.value)));
                                    vm.task.finish_time = dateFormat(new Date(vm.edit.finish_time.value));
                                    Tasks.update({
                                        eventId: $location.search().eventId,
                                        taskId: $location.search().taskId
                                    }, {
                                        finish_time: dateFormat(new Date(vm.edit.finish_time.value))
                                    }, function (response) {
                                        vm.edit.finish_time.status = false;
                                    })
                                }
                            },
                            users: {
                                items: [],
                                status: false,
                                changeStatus: function () {
                                    vm.edit.users.status = !vm.edit.users.status;
                                    vm.edit.users.items = [];
                                },
                                update: function () {

                                }
                            }
                        };
                    });
                    UsersInTask.query({
                        eventId: $location.search().eventId,
                        taskId: $location.search().taskId
                    }, function (response) {
                        vm.users = JSON.parse(angular.toJson(response));
                        vm.isParticipant = false;
                        var id = Auth.getUserId();
                        for (var i = 0, len = vm.users.length; i < len; i++) {
                            if (vm.users[i].id == id) {
                                vm.isParticipant = true;
                                break;
                            }
                        }
                        if (!vm.isParticipant) {
                            vm.isParticipant = false;
                        }
                    });
                }
            };


            vm.isUserInTask = function (id) {
                if (vm.users) {
                    for (var i = 0, len = vm.users.length; i < len; i++) {
                        if (vm.users[i].id == id) {
                            return true;
                        }
                    }
                    return false;
                }
            };

            vm.isUserTaskHeader = function (id) {
                return vm.task.task_header == id;
            };

            vm.isThisUser = function (id) {
                return Auth.getUserId() == id;
            };


            vm.addUser = function (id) {
                UsersInTask.save({eventId: $location.search().eventId, taskId: $location.search().taskId}, {
                    user: id
                }, function (response) {
                    var user = JSON.parse(angular.toJson(response));
                    vm.users.push(user);
                })
            };

            var dateFormat = function (date) {
                return date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) +
                    '-' + ('0' + date.getDate()).slice(-2);
            };


            vm.statuses = ['COMPLETED', 'DELAYED', 'IN_PROGRESS'];

            vm.removeUser = function (index) {
                var user = vm.users[index];
                if (user.id == vm.task.task_header.id) {
                    alert("Нельзя удалить руководителя из задания");
                    return;
                }
                UsersInTask.delete({
                    eventId: $location.search().eventId,
                    taskId: $location.search().taskId,
                    userId: user.id
                });
                vm.users.splice(index, 1);
                if (vm.isThisUser(user.id)) {
                    vm.init();
                }
            };

        });
})();
