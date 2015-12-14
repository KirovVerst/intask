(function () {
    'use strict';

    angular
        .module('application.events.controllers')
        .controller('CurrentEventController', function (Events, $http, $scope, Auth, $window, $routeParams, UsersInEvent, $location) {
            var vm = this;
            vm.today = new Date();
            vm.isLoggedIn = !!Auth.getToken();

            vm.init = function () {
                var eventId = $location.search().eventId;
                if (eventId) {
                    Events.get({id: eventId}, function (data) {
                        vm.event = JSON.parse(angular.toJson(data));
                        vm.event.finish_time = new Date(vm.event.finish_time);
                        vm.isEventHeader = Auth.getUserId() == data.event_header.id;
                        vm.edit = {
                            description: {
                                value: angular.copy(vm.event.description),
                                status: false,
                                changeStatus: function () {
                                    vm.edit.description.status = !vm.edit.description.status;
                                    vm.edit.description.value = angular.copy(vm.event.description);
                                },
                                update: function () {
                                    vm.event.description = vm.edit.description.value;
                                    Events.update({id: vm.event.id}, {
                                        description: vm.event.description
                                    }, function (response) {
                                        vm.edit.description.status = false;
                                    })
                                }
                            },
                            finish_time: {
                                value: angular.copy(vm.event.finish_time),
                                status: false,
                                changeStatus: function () {
                                    vm.edit.finish_time.status = !vm.edit.finish_time.status;
                                    vm.edit.finish_time.value = angular.copy(vm.event.finish_time);
                                },
                                update: function () {
                                    console.log(dateFormat(new Date(vm.edit.finish_time.value)));
                                    vm.event.finish_time = dateFormat(new Date(vm.edit.finish_time.value));
                                    Events.update({
                                        id: $location.search().eventId
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
                    vm.users = [];
                    UsersInEvent.query({eventId: eventId}, function (response) {
                        angular.forEach(response, function (item) {
                            vm.users.push(item);
                        })
                    });
                }
                vm.newUser = {};
                var taskId = $location.search().taskId;
                if (taskId) {
                    vm.task = true;
                    vm.eventClass = "col-sm-8";
                    vm.tasksClass = "col-sm-11";
                } else {
                    vm.task = false;
                    vm.newTask = false;
                    vm.eventClass = "col-sm-12";
                    vm.tasksClass = "col-sm-10";
                }


            };


            vm.editDescription = function () {
                console.log("vndfkvfd");
                vm.editDescriptionValue = !editDescriptionValue;
            };

            var changeClasses = function () {
                vm.eventClass = (vm.eventClass == "col-sm-12") ? "col-sm-8" : "col-sm-12";
                vm.tasksClass = (vm.tasksClass == "col-sm-10") ? "col-sm-11" : "col-sm-10";
            };

            vm.isThisUser = function (id) {
                return Auth.getUserId() == id;
            };

            vm.setNewTask = function () {
                if (!vm.task && !vm.newTask) {
                    changeClasses();
                }
                vm.newTask = true;
                vm.task = false;
            };
            vm.popNewTask = function () {
                vm.newTask = null;
                changeClasses();
            };

            vm.setTask = function () {
                if (!vm.task && !vm.newTask) {
                    changeClasses();
                }
                vm.task = true;
                vm.newTask = false;

            };

            vm.popTask = function () {
                vm.task = false;
                $location.search({eventId: vm.event.id});
                changeClasses();
            };

            vm.inviteUser = function () {
                UsersInEvent.save({eventId: $routeParams.eventId}, vm.newUser, function (response) {
                    vm.event.invited_users.push(vm.newUser.email);
                    vm.newUser = {};
                });
            };
            vm.popNewUser = function () {
                vm.newUser = null;
            };

            vm.editFormEvent = false;
            vm.setEditFormEvent = function () {
                vm.editFormEvent = true;
            };
            vm.popEditFormEvent = function () {
                vm.editFormEvent = false;
            };
            var dateFormat = function (date) {
                return date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) +
                    '-' + ('0' + date.getDate()).slice(-2);
            };
            vm.updateEvent = function () {
                Events.update({id: vm.event.id}, {
                    title: vm.event.title,
                    description: vm.event.description,
                    finish_time: dateFormat(new Date(vm.event.finish_time)),
                    event_header: parseInt(vm.event.event_header.id),
                    status: vm.event.status
                }).$promise.then(function (data) {
                    vm.isEventUpdated = true;
                    vm.result_message = "Изменения сохранены.";
                })
            };

            vm.statuses = ['COMPLETED', 'DELAYED', 'IN_PROGRESS'];

            vm.removeUser = function (index) {
                var user = vm.users[index];
                if (user.id == vm.event.event_header.id) {
                    alert("Нельзя удалить руководителя из события");
                    return;
                }
                UsersInEvent.delete({eventId: $routeParams.eventId, userId: user.id});
                if (!vm.isEventHeader) {
                    $window.location = "/";
                }
                vm.users.splice(index, 1);
            };

            vm.removeInvitedUser = function (index) {
                var email = vm.event.invited_users[index];
                $http.post('api/events/' + vm.event.id + '/invited_users/', {email: email}).success(function (data) {
                    vm.event.invited_users.splice(index, 1);
                })
            }


        });
})();
