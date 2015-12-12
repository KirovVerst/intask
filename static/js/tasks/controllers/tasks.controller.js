/**
 * Created by Kirov on 19/11/15.
 */
(function () {
    'use strict';

    angular.module('application.tasks.controllers')
        .controller('TasksController', function (Tasks, Events, $routeParams, $window, Auth, $filter, $location, UsersInTask) {

            var orderBy = $filter('orderBy');
            var vm = this;

            vm.init = function () {
                vm.eventId = $location.search().eventId;
                if (vm.eventId) {
                    vm.newTask = {};
                    vm.myTasks = [];
                    vm.otherTasks = [];
                    Tasks.query({eventId: vm.eventId}, function (response) {
                        angular.forEach(response, function (item) {
                            item.task_header.id == Auth.getUserId() ? vm.myTasks.push(item) : vm.otherTasks.push(item);
                        });
                    });
                }
            };


            vm.setTask = function (task) {
                vm.task = task;
            };

            vm.popTask = function () {
                vm.task = null;
            };

            var dateFormat = function (date) {
                return date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) +
                    '-' + ('0' + date.getDate()).slice(-2);
            };

            vm.createTask = function () {
                var users = vm.newTask.users;
                console.log(users);
                delete vm.newTask.users;
                vm.newTask.finish_time = dateFormat(new Date(vm.newTask.finish_time));
                Tasks.save({eventId: vm.eventId}, vm.newTask, function (response) {
                    var task = JSON.parse(angular.toJson(response));
                    if (task.task_header.id == Auth.getUserId()) {
                        vm.myTasks.push(angular.copy(task));
                    } else {
                        vm.otherTasks.push(angular.copy(task));
                    }
                    angular.forEach(users, function (item) {
                        UsersInTask.save({eventId: vm.eventId, taskId: task.id}, {user: parseInt(item)});
                    })
                });
            };

            vm.removeTask = function (index, tasks) {
                Tasks.delete({eventId: vm.eventId, taskId: tasks[index].id});
                tasks.splice(index, 1);
            };

            vm.orderMyTask = function (predicate) {
                vm.reverseMyTask = (vm.predicateMyTask === predicate) ? !vm.reverseMyTask : false;
                vm.classMyTask = vm.reverseMyTask ? "glyphicon glyphicon-chevron-up" : "glyphicon glyphicon-chevron-down";
                vm.predicateMyTask = predicate;
                vm.myTasks = orderBy(vm.myTasks, predicate, vm.reverseMyTask);
            };


            vm.orderOtherTask = function (predicate) {
                vm.reverseOtherTask = (vm.predicateOtherTask === predicate) ? !vm.reverseOtherTask : false;
                vm.predicateOtherTask = predicate;
                vm.classOtherTask = vm.reverseOtherTask ? "glyphicon glyphicon-chevron-up" : "glyphicon glyphicon-chevron-down";

                vm.otherTasks = orderBy(vm.otherTasks, predicate, vm.reverseOtherTask);
            };

        })
})();
