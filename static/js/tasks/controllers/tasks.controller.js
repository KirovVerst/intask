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
                    vm.myTasks = {
                        active: {
                            is_shown: false,
                            toggle: function () {
                                vm.myTasks.active.is_shown = !vm.myTasks.active.is_shown;
                            },
                            items: [],
                            reversed: false,
                            predicate: 'title',
                            class: "",
                            order: function (predicate) {
                                vm.myTasks.active.reversed = (vm.myTasks.active.predicate === predicate) ? !vm.myTasks.active.reversed : false;
                                vm.myTasks.active.class = vm.myTasks.active.reversed ? "glyphicon glyphicon-chevron-up" : "glyphicon glyphicon-chevron-down";
                                vm.myTasks.active.predicate = predicate;
                                vm.myTasks.active.items = orderBy(vm.myTasks.active.items, predicate, vm.myTasks.active.reversed);
                            }
                        },
                        completed: {
                            is_shown: false,
                            toggle: function () {
                                vm.myTasks.completed.is_shown = !vm.myTasks.completed.is_shown;
                            },
                            items: [],
                            reversed: false,
                            predicate: 'title',
                            class: "",
                            order: function (predicate) {
                                vm.myTasks.completed.reversed = (vm.myTasks.completed.predicate === predicate) ? !vm.myTasks.completed.reversed : false;
                                vm.myTasks.completed.class = vm.myTasks.completed.reversed ? "glyphicon glyphicon-chevron-up" : "glyphicon glyphicon-chevron-down";
                                vm.myTasks.completed.predicate = predicate;
                                vm.myTasks.completed.items = orderBy(vm.myTasks.completed.items, predicate, vm.myTasks.completed.reversed);
                            }
                        }
                    };
                    vm.otherTasks = {
                        active: {
                            is_shown: false,
                            toggle: function () {
                                vm.otherTasks.active.is_shown = !vm.otherTasks.active.is_shown;
                            },
                            items: [],
                            reversed: false,
                            predicate: 'title',
                            class: "",
                            order: function (predicate) {
                                vm.otherTasks.active.reversed = (vm.otherTasks.active.predicate === predicate) ? !vm.otherTasks.active.reversed : false;
                                vm.otherTasks.active.class = vm.otherTasks.active.reversed ? "glyphicon glyphicon-chevron-up" : "glyphicon glyphicon-chevron-down";
                                vm.otherTasks.active.predicate = predicate;
                                vm.otherTasks.active.items = orderBy(vm.otherTasks.active.items, predicate, vm.otherTasks.active.reversed);
                            }
                        },
                        completed: {
                            is_shown: false,
                            toggle: function () {
                                vm.otherTasks.completed.is_shown = !vm.otherTasks.completed.is_shown;
                            },
                            items: [],
                            reversed: false,
                            predicate: 'title',
                            class: "",
                            order: function (predicate) {
                                vm.otherTasks.completed.reversed = (vm.otherTasks.completed.predicate === predicate) ? !vm.otherTasks.completed.reversed : false;
                                vm.otherTasks.completed.class = vm.otherTasks.completed.reversed ? "glyphicon glyphicon-chevron-up" : "glyphicon glyphicon-chevron-down";
                                vm.otherTasks.completed.predicate = predicate;
                                vm.otherTasks.completed.items = orderBy(vm.otherTasks.completed.items, predicate, vm.otherTasks.completed.reversed);
                            }
                        }
                    };
                    Tasks.query({eventId: vm.eventId}, function (response) {
                        angular.forEach(response, function (item) {
                            if (item.task_header.id == Auth.getUserId()) {
                                (item.status == "COMPLETED") ? vm.myTasks.completed.items.push(item) : vm.myTasks.active.items.push(item)
                            } else {
                                (item.status == "COMPLETED") ? vm.otherTasks.completed.items.push(item) : vm.otherTasks.active.items.push(item)
                            }
                        });
                    });
                }
            };


            vm.setTask = function (taskId) {
                $location.search({eventId: vm.eventId, taskId: taskId});
                vm.task = taskId;
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

            vm.reverse = false;
            vm.predicate = 'title';

            vm.orderTasks = function (predicate, tasks) {
                console.log(predicate);
                vm.reverse = (vm.predicate === predicate) ? !vm.reverse : false;
                vm.class = vm.reverse ? "glyphicon glyphicon-chevron-up" : "glyphicon glyphicon-chevron-down";
                vm.predicate = predicate;
                tasks = orderBy(tasks, predicate, vm.reverse);
            };


            vm.orderOtherTask = function (predicate) {
                vm.reverseOtherTask = (vm.predicateOtherTask === predicate) ? !vm.reverseOtherTask : false;
                vm.predicateOtherTask = predicate;
                vm.classOtherTask = vm.reverseOtherTask ? "glyphicon glyphicon-chevron-up" : "glyphicon glyphicon-chevron-down";

                vm.otherTasks = orderBy(vm.otherTasks, predicate, vm.reverseOtherTask);
            };

        })
})();
