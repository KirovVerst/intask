(function () {
    'use strict';

    angular
        .module('application.events.controllers')
        .controller('CurrentEventController', function (Events, $http, $scope, Auth, $window, $routeParams, UsersInEvent, $location) {
            var vm = this;
            vm.today = new Date();
            vm.isLoggedIn = !!Auth.getToken();

            vm.init = function (eventId) {
                if (eventId) {
                    $location.search({eventId: eventId});

                    Events.get({id: eventId}, function (data) {
                        vm.event = JSON.parse(angular.toJson(data));
                        vm.event.finish_time = new Date(vm.event.finish_time);
                        vm.isEventHeader = Auth.getUserId() == data.event_header.id;
                    });

                    vm.users = UsersInEvent.query({eventId: $routeParams.eventId});
                }

                vm.task = false;
                vm.newTask = false;
                vm.eventClass = "col-sm-12";
                vm.tasksClass = "col-sm-10"
            };

            var changeClasses = function () {
                vm.eventClass = (vm.eventClass == "col-sm-12") ? "col-sm-8" : "col-sm-12";
                vm.tasksClass = (vm.tasksClass == "col-sm-10") ? "col-sm-11" : "col-sm-10";
            };


            vm.isThisUser = function (id) {
                return Auth.getUserId() == id;
            };

            vm.setNewTask = function () {
                vm.newTask = true;
                changeClasses();
            };
            vm.popNewTask = function () {
                vm.newTask = null;
                changeClasses();
            };


            vm.newUser = null;
            vm.setNewUser = function () {
                vm.newUser = {};
            };
            vm.inviteUser = function () {
                UsersInEvent.save({eventId: $routeParams.eventId}, vm.newUser);
                vm.event.invited_users.push(vm.newUser.email);
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
