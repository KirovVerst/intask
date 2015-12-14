/**
 * Created by Kirov on 19/11/15.
 */
(function () {
    'use strict';

    angular.module('application.tasks.controllers')
        .controller('SubtasksController', function (Tasks, Events, Subtasks, $routeParams, $window, Auth, $filter, $location) {

            var orderBy = $filter('orderBy');
            var vm = this;

            vm.init = function () {
                vm.params = $location.search();
                if (vm.params.eventId && vm.params.taskId) {
                    vm.activeSubtasks = [];
                    vm.completedSubtasks = [];
                    vm.newSubtask = {};
                    Subtasks.query({eventId: vm.params.eventId, taskId: vm.params.taskId}, function (response) {
                        angular.forEach(response, function (item) {
                            item.is_completed ? vm.completedSubtasks.push(item) : vm.activeSubtasks.push(item);
                        });
                    });
                }
            };

            var dateFormat = function (date) {
                return date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) +
                    '-' + ('0' + date.getDate()).slice(-2);
            };

            vm.createSubtask = function () {
                Subtasks.save({
                    eventId: vm.params.eventId,
                    taskId: vm.params.taskId
                }, vm.newSubtask, function (response) {
                    vm.activeSubtasks.push(JSON.parse(angular.toJson(response)));
                    vm.newSubtask = {};
                });
            };

            vm.changeSubtaskStatus = function (index, value) {
                var subtask = {};
                if (value) {
                    subtask = angular.copy(vm.activeSubtasks[index]);
                    subtask.is_completed = value;
                    vm.activeSubtasks.splice(index, 1);
                    vm.completedSubtasks.push(subtask);
                } else {
                    subtask = angular.copy(vm.completedSubtasks[index]);
                    subtask.is_completed = value;
                    vm.completedSubtasks.splice(index, 1);
                    vm.activeSubtasks.push(subtask);
                }
                Subtasks.update({eventId: vm.params.eventId, taskId: vm.params.taskId, subtaskId: subtask.id}, {
                    is_completed: value
                }, function (response) {
                })
            };

            vm.removeSubtask = function (index, is_active) {
                var subtask = {};
                console.log(index);
                console.log(is_active);
                if (is_active) {
                    subtask = vm.activeSubtasks[index];
                    vm.activeSubtasks.splice(index, 1);
                } else {
                    subtask = vm.completedSubtasks[index];
                    vm.completedSubtasks.splice(index, 1);
                }
                Subtasks.delete({eventId: vm.params.eventId, taskId: vm.params.taskId, subtaskId: subtask.id});
            };


            vm.orderSubtask = function (predicate) {
                vm.reverse = (vm.predicate === predicate) ? !vm.reverse : false;
                vm.class = vm.reverse ? "glyphicon glyphicon-chevron-up" : "glyphicon glyphicon-chevron-down";
                vm.predicate = predicate;
                vm.subtasks = orderBy(vm.subtasks, predicate, vm.reverse);
            };

            vm.currentSubtask = false;

            vm.setEditFormSubtask = function (index) {
                vm.currentSubtask = vm.subtasks[index];
            };
            vm.popEditFormSubtask = function () {
                vm.currentSubtask = false;
            };

            vm.updateSubtask = function () {
                vm.currentSubtask = dateFormat(new Date(vm.currentSubtask));
                Subtasks.update({
                    eventId: $routeParams.eventId,
                    taskId: $routeParams.taskId,
                    subtaskId: vm.currentSubtask.id
                }, vm.currentSubtask).$promise.then(function (response) {
                    if (response.$status == 200) {
                        vm.message = "Обновлено";
                        vm.class = "alert-success";
                        vm.errors = null;
                    } else {
                        vm.message = "Ошибка : " + response.$status;
                        vm.class = "alert-danger";
                        vm.errors = null;
                    }
                });
            }


        })
})();
