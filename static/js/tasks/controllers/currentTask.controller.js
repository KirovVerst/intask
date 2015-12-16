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
                        vm.task.is_finished = (vm.task.status == "COMPLETED" );

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
                            title: {
                                value: angular.copy(vm.task.title),
                                status: false,
                                changeStatus: function () {
                                    vm.edit.title.status = !vm.edit.title.status;
                                    vm.edit.title.value = angular.copy(vm.task.title);
                                    vm.edit.title.errors = [];
                                },
                                update: function () {
                                    /*if (vm.edit.title.value.length > 100) {
                                        vm.edit.title.status = true;
                                        vm.edit.title.errors = ["Название должно содержать не более 100 символов."];
                                        return;
                                    }*/
                                    Tasks.update({
                                        eventId: $location.search().eventId,
                                        taskId: $location.search().taskId
                                    }, {
                                        title: vm.edit.title.value
                                    }, function (response) {
                                        if (response.$status >= 500) {
                                            vm.edit.title.status = true;
                                            vm.edit.title.errors = ["Server Error"];
                                        } else if (response.$status >= 400) {
                                            vm.edit.title.status = true;
                                            vm.edit.title.errors = response.title;
                                        } else {
                                            vm.edit.title.status = false;
                                            vm.edit.title.errors = [];
                                            vm.task.title = vm.edit.title.value;
                                        }
                                    })
                                }
                            },
                            finish_time: {
                                value: angular.copy(vm.task.finish_time),
                                status: false,
                                changeStatus: function () {
                                    vm.edit.finish_time.status = !vm.edit.finish_time.status;
                                    vm.edit.finish_time.value = angular.copy(vm.task.finish_time);
                                },
                                update: function () {
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
                            is_finished: {
                                value: angular.copy(vm.task.is_finished),
                                status: false,
                                items: [{
                                    item: true,
                                    text: "Завершено"
                                },
                                    {
                                        item: false,
                                        text: "Активно"
                                    }
                                ],
                                changeStatus: function () {
                                    vm.edit.is_finished.status = !vm.edit.is_finished.status;
                                    vm.edit.is_finished.value = angular.copy(vm.task.is_finished);
                                },
                                update: function () {
                                    var value = (vm.edit.is_finished.value) ? "COMPLETED" : "IN_PROGRESS";
                                    Tasks.update({
                                        eventId: $location.search().eventId,
                                        taskId: $location.search().taskId
                                    }, {
                                        status: value
                                    }, function (response) {
                                        if (response.$status >= 500) {
                                            vm.edit.is_finished.status = true;
                                            vm.edit.is_finished.errors = ["Server Error"];
                                        } else if (response.$status >= 400) {
                                            vm.edit.is_finished.status = true;
                                            vm.edit.is_finished.errors = response.is_finished;
                                        } else {
                                            vm.task.is_finished = vm.edit.is_finished.value;
                                            vm.edit.is_finished.status = false;
                                            vm.edit.is_finished.errors = [];
                                        }
                                    })
                                }
                            },
                            is_public: {
                                value: angular.copy(vm.task.is_public),
                                status: false,
                                items: [{
                                    item: true,
                                    text: "Публично"
                                },
                                    {
                                        item: false,
                                        text: "Приватно"
                                    }
                                ],
                                changeStatus: function () {
                                    vm.edit.is_public.status = !vm.edit.is_public.status;
                                    vm.edit.is_public.value = angular.copy(vm.task.is_public);
                                },
                                update: function () {
                                    Tasks.update({
                                        eventId: $location.search().eventId,
                                        taskId: $location.search().taskId
                                    }, {
                                        is_public: vm.edit.is_public.value
                                    }, function (response) {
                                        vm.task.is_public = vm.edit.is_public.value;
                                        if (response.$status >= 500) {
                                            vm.edit.is_public.status = true;
                                            vm.edit.is_public.errors = ["Server Error"];
                                        } else if (response.$status >= 400) {
                                            vm.edit.is_public.status = true;
                                            vm.edit.is_public.errors = response.is_public;
                                        } else {
                                            vm.edit.is_public.status = false;
                                            vm.edit.is_public.errors = [];
                                        }
                                    })
                                }
                            },
                            task_header: {
                                value: angular.copy(vm.task.task_header.id),
                                status: false,
                                changeStatus: function () {
                                    vm.edit.task_header.status = !vm.edit.task_header.status;
                                    vm.edit.task_header.value = angular.copy(vm.task.task_header.id);
                                },
                                update: function () {
                                    Tasks.update({
                                        eventId: $location.search().eventId,
                                        taskId: $location.search().taskId
                                    }, {
                                        task_header: vm.edit.task_header.value
                                    }, function (response) {
                                        if (response.$status >= 500) {
                                            vm.edit.task_header.status = true;
                                            vm.edit.task_header.errors = ["Server Error"];
                                        } else if (response.$status >= 400) {
                                            vm.edit.task_header.status = true;
                                            vm.edit.task_header.errors = response.task_header;
                                        } else {
                                            $route.reload();
                                            vm.edit.task_header.status = false;
                                            vm.edit.task_header.errors = [];
                                        }
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
                return vm.task.task_header.id == id;
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

            vm.escape = function () {
                UsersInTask.delete({
                    eventId: $location.search().eventId,
                    taskId: $location.search().taskId,
                    userId: Auth.getUserId()
                }, function (response) {
                    if (vm.task.is_public) {
                        vm.init();
                    } else {
                        var params = $location.search();
                        delete params.taskId;
                        $location.search(params);
                        $route.reload();
                    }

                });

            };


            vm.statuses = ['COMPLETED', 'DELAYED', 'IN_PROGRESS'];

            vm.removeUser = function (index) {
                var user = vm.users[index];
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
