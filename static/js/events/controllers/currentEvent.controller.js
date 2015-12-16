(function () {
    'use strict';

    var update = function (obj, resource, params, data) {
        console.log(obj);
        resource.update(params, data,
            function (response) {
                obj.isRequestSent = true;
                obj.success = true;
                var result = JSON.parse(angular.toJson(response));
                if (response.$status >= 500) {
                    obj.success = false;
                    obj.message = "Ошибка на сервере";
                } else if (response.$status >= 400) {
                    obj.success = false;
                    obj.errors = result;
                    obj.message = "Изменения не сохранены.";
                } else if (response.$status >= 200) {
                    obj.message = "Изменения сохранены";
                    delete obj.errors;
                }
            });
    };

    angular
        .module('application.events.controllers')
        .controller('CurrentEventController', function (Events, Tasks, $http, $scope, Auth, $route, $window, $routeParams, UsersInEvent, $location) {
            var vm = this;
            vm.today = new Date();
            vm.isLoggedIn = !!Auth.getToken();

            vm.init = function () {
                var eventId = $location.search().eventId;
                if (eventId) {
                    Events.get({id: eventId}, function (data) {
                        vm.event = JSON.parse(angular.toJson(data));
                        vm.event.is_finished = (vm.event.status == "COMPLETED" );
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
                            title: {
                                value: angular.copy(vm.event.title),
                                status: false,
                                changeStatus: function () {
                                    vm.edit.title.status = !vm.edit.title.status;
                                    vm.edit.title.value = angular.copy(vm.event.title);
                                    vm.edit.title.errors = [];
                                },
                                update: function () {
                                    Events.update({id: vm.event.id}, {
                                        title: vm.edit.title.value
                                    }, function (response) {
                                        if (response.$status >= 500) {
                                            vm.edit.title.status = true;
                                            vm.edit.title.errors = ["Server Error"];
                                        } else if (response.$status >= 400) {
                                            vm.edit.title.status = true;
                                            vm.edit.title.errors = response.title;
                                        } else {
                                            vm.event.title = vm.edit.title.value;
                                            vm.edit.title.status = false;
                                            vm.edit.title.errors = [];
                                        }
                                    })
                                }
                            },
                            is_finished: {
                                value: angular.copy(vm.event.is_finished),
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
                                    vm.edit.is_finished.value = angular.copy(vm.event.is_finished);
                                },
                                update: function () {
                                    vm.event.is_finished = vm.edit.is_finished.value;
                                    var value = (vm.event.is_finished) ? "COMPLETED" : "IN_PROGRESS";
                                    Events.update({id: vm.event.id}, {
                                        status: value
                                    }, function (response) {
                                        if (response.$status >= 500) {
                                            vm.edit.is_finished.status = true;
                                            vm.edit.is_finished.errors = ["Server Error"];
                                        } else if (response.$status >= 400) {
                                            vm.edit.is_finished.status = true;
                                            vm.edit.is_finished.errors = response.is_finished;
                                        } else {
                                            vm.edit.is_finished.status = false;
                                            vm.edit.is_finished.errors = [];
                                        }
                                    })
                                }
                            },
                            event_header: {
                                value: angular.copy(vm.event.event_header.id),
                                status: false,
                                changeStatus: function () {
                                    vm.edit.event_header.status = !vm.edit.event_header.status;
                                    vm.edit.event_header.value = angular.copy(vm.event.event_header.id);
                                },
                                update: function () {
                                    Events.update({id: vm.event.id}, {
                                        event_header: vm.edit.event_header.value
                                    }, function (response) {
                                        if (response.$status >= 500) {
                                            vm.edit.event_header.status = true;
                                            vm.edit.event_header.errors = ["Server Error"];
                                        } else if (response.$status >= 400) {
                                            vm.edit.event_header.status = true;
                                            vm.edit.event_header.errors = response.event_header;
                                        } else {
                                            $route.reload();
                                            vm.edit.event_header.status = false;
                                            vm.edit.event_header.errors = [];
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
                                    vm.newUser = {};
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
                    Tasks.get({eventId: eventId, taskId: taskId}, function (response) {
                        if (response.$status >= 400) {
                            vm.task = false;
                            vm.newTask = false;
                            vm.eventClass = "col-sm-12";
                            vm.tasksClass = "col-sm-10";
                            var params = $location.search();
                            delete params.taskId;
                            $location.search(params);
                        } else {
                            vm.task = true;
                            vm.eventClass = "col-sm-8";
                            vm.tasksClass = "col-sm-11";
                        }
                    });
                } else {
                    vm.task = false;
                    vm.newTask = false;
                    vm.eventClass = "col-sm-12";
                    vm.tasksClass = "col-sm-10";
                }
            };

            vm.setEvent = function () {

            };

            vm.popEvent = function () {
                $location.search({});
            };


            vm.editDescription = function () {
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
                if (vm.event.invited_users.indexOf(vm.newUser.email) != -1) {
                    vm.newUser.error = "Email has already been added in list of invited users.";
                    return;
                }
                UsersInEvent.save({eventId: $routeParams.eventId}, vm.newUser, function (response) {
                    if (response.error) {
                        vm.newUser = {
                            error: response.error
                        };
                    } else {
                        vm.event.invited_users.push(vm.newUser.email);
                        vm.newUser = {};
                    }

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
                UsersInEvent.delete({eventId: $routeParams.eventId, userId: user.id});
                vm.users.splice(index, 1);
            };

            vm.escape = function () {
                if (vm.isEventHeader && vm.users.length > 1) {
                    alert("Руководитель не может покинуть событие. Назначьте другого руководителя.");
                    return;
                }
                if (vm.isEventHeader) {
                    var q = confirm("Вы – единственный участник этого события. Если Вы выйдете, событие будет удалено. " +
                        "Хотите выйти из события?");
                    if (q) {
                        Events.delete({id: vm.event.id});
                        $window.location = "/";
                    }
                } else {
                    var f = confirm("Хотите выйти из события? Вернуться возможно будет непросто!");
                    if (f) {
                        UsersInEvent.delete({eventId: vm.event.id, userId: Auth.getUserId()});
                        $window.location = "/";
                    }
                }
            };


            vm.removeInvitedUser = function (index) {
                var email = vm.event.invited_users[index];
                $http.post('api/events/' + vm.event.id + '/invited_users/', {email: email}).success(function (data) {
                    vm.event.invited_users.splice(index, 1);
                })
            }


        });
})();
