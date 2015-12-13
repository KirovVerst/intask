(function () {
    'use strict';

    angular
        .module('application.tasks.controllers')
        .controller('CurrentTaskController', function (Events, Tasks, $http, $scope, $location, Auth, $window,
                                                       $routeParams, UsersInTask, Subtasks, $timeout) {
            var vm = this;
            vm.today = new Date();
            vm.isLoggedIn = !!Auth.getToken();

            vm.init = function () {
                if ($location.search().taskId) {
                    Tasks.get({
                        eventId: $location.search().eventId,
                        taskId: $location.search().taskId
                    }, function (response) {
                        vm.task = JSON.parse(angular.toJson(response));
                        vm.title = vm.task.title;
                        vm.task.finish_time = new Date(vm.task.finish_time);
                        vm.isTaskHeader = Auth.getUserId() == vm.task.task_header.id;
                    });
                    UsersInTask.query({
                        eventId: $location.search().eventId,
                        taskId: $location.search().taskId
                    }, function (response) {
                        vm.users = JSON.parse(angular.toJson(response));
                    });

                    Subtasks.query({
                        eventId: $location.search().eventId,
                        taskId: $location.search().taskId
                    }, function (response) {
                        vm.subtasks = JSON.parse(angular.toJson(response));
                    });
                    vm.edit = false;
                }
            };

            vm.editMode = function () {
                vm.edit = !vm.edit;
                vm.copyTask = angular.copy(vm.task);
                vm.title = vm.edit ? "Редактирование" : vm.task.title;
                vm.resultMessage = "";
            };

            vm.popTask = function () {
                vm.task = null;
            };

            vm.isThisUser = function (id) {
                return Auth.getUserId() == id;
            };

            vm.newSubtask = false;
            vm.setNewSubtask = function () {
                vm.newSubtask = true;
            };
            vm.popNewSubtask = function () {
                vm.newSubtask = false;
            };


            vm.newUser = null;
            vm.setNewUser = function () {
                vm.newUser = {};
            };
            vm.addUser = function () {

            };

            vm.popNewUser = function () {
                vm.newUser = false;
            };

            vm.editFormTask = false;
            vm.setEditFormTask = function () {
                vm.editFormTask = true;
            };
            vm.popEditFormTask = function () {
                vm.editFormTask = false;
            };
            var dateFormat = function (date) {
                return date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) +
                    '-' + ('0' + date.getDate()).slice(-2);
            };
            vm.updateTask = function () {
                Tasks.update({eventId: $location.search().eventId, taskId: vm.copyTask.id}, {
                    title: vm.copyTask.title,
                    description: vm.copyTask.description,
                    finish_time: dateFormat(new Date(vm.copyTask.finish_time)),
                    task_header: parseInt(vm.copyTask.task_header.id),
                    status: vm.copyTask.status,
                    is_public: vm.copyTask.is_public
                }, function (response) {
                    if (response.$status == 200) {
                        vm.task = JSON.parse(angular.toJson(response));
                        vm.resultMessage = "Изменения сохранены.";
                        $timeout(function () {
                            vm.resultMessage = "";
                        }, 3000);
                        vm.updateClass = "alert-success";
                    } else {
                        vm.updateClass = "alert-danger";
                        vm.resultMessage = "Ошибка " + response.$status;
                    }
                })
            };

            vm.statuses = ['COMPLETED', 'DELAYED', 'IN_PROGRESS'];

            vm.removeUser = function (index) {
                var user = vm.users[index];
                if (user.id == vm.task.task_header.id) {
                    alert("Нельзя удалить руководителя из задания");
                    return;
                }
                UsersInTask.delete({
                    eventId: $routeParams.eventId,
                    taskId: $routeParams.taskId,
                    userId: user.id
                });
                if (!(vm.isEventHeader || vm.isTaskHeader)) {
                    $window.location = "/";
                }
                vm.users.splice(index, 1);
            };


            vm.removeSubtask = function (index) {
                var subtask = vm.subtasks[index];
                Subtasks.delete({eventId: $routeParams.eventId, taskId: $routeParams.taskId, subtaskId: subtask.id});
                vm.subtasks.splice(index, 1);
            }
        });
})();
