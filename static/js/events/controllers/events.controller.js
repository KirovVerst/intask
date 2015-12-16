(function () {
    'use strict';


    angular
        .module('application.events.controllers')
        .controller('EventsController', function (Events, $http, $scope, Auth, $window, $routeParams, $filter, $location) {

            var orderBy = $filter('orderBy');

            var vm = this;
            vm.today = new Date();
            vm.isLoggedIn = !!Auth.getToken();
            vm.newEvent = false;
            vm.showMyEvents = false;
            vm.showOtherEvents = false;

            vm.toggleEvents = function (isMyEvents) {
                isMyEvents ? vm.showMyEvents = !vm.showMyEvents : vm.showOtherEvents = !vm.showOtherEvents;
            };

            vm.init = function () {
                Auth.check();
                Events.query(function (response) {
                    var userId = Auth.getUserId();
                    var data = JSON.parse(angular.toJson(response));
                    vm.myEvents = [];
                    vm.otherEvents = [];
                    for (var i in data) {

                        if (data[i].event_header.id == userId) {
                            vm.myEvents.push(data[i]);
                        }
                        else {
                            vm.otherEvents.push(data[i]);
                        }
                    }
                });
                if ($location.search().eventId) {
                    Events.get({id: $location.search().eventId}, function (response) {
                        if (response.$status >= 400) {
                            vm.event = false;
                            $location.search({});
                        } else {
                            vm.event = $location.search().eventId;
                        }
                    });
                }
                if ($location.search().newEvent) {
                    vm.newEvent = {
                        finish_time: new Date()
                    }
                }
            };

            vm.setEvent = function (eventId) {
                vm.event = eventId;
                $location.search({eventId: eventId});
            };

            vm.popEvent = function () {
                vm.event = false;
                $location.search({});
            };

            vm.setNewEvent = function () {
                $location.search({newEvent: true});
                vm.newEvent = {
                    finish_time: new Date()
                }
            };
            vm.popNewEvent = function () {
                $location.search({});
                vm.newEvent = null;
            };


            var dateFormat = function (date) {
                return date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) +
                    '-' + ('0' + date.getDate()).slice(-2);
            };
            vm.createEvent = function () {
                vm.newEvent.event_header = Auth.getUserId();
                vm.newEvent.finish_time = dateFormat(new Date(vm.newEvent.finish_time));
                Events.save(vm.newEvent, function (response) {
                    vm.popNewEvent();
                    vm.setEvent(response.id);

                });
            };


            vm.deleteEvent = function () {
                var f = confirm("Вы действительно хотите удалить событие ?");
                if (f) {
                    Events.delete({id: vm.event});
                    $window.location = "/";
                }
            };

            vm.redirectToEventPage = function (eventId) {
                $window.location = '/events/' + eventId + '/';
            };

            vm.predicateMyEvent = 'title';
            vm.reverseMyEvent = false;
            vm.orderMyEvent = function (predicate) {
                vm.reverseMyEvent = (vm.predicateMyEvent === predicate) ? !vm.reverseMyEvent : false;
                vm.classMyEvent = vm.reverseMyEvent ? "glyphicon glyphicon-chevron-up" : "glyphicon glyphicon-chevron-down";
                vm.predicateMyEvent = predicate;
                vm.myEvents = orderBy(vm.myEvents, predicate, vm.reverseMyEvent);
            };

            vm.predicateOtherEvent = 'title';
            vm.reverseOtherEvent = false;
            vm.orderOtherEvent = function (predicate) {
                vm.reverseOtherEvent = (vm.predicateOtherEvent === predicate) ? !vm.reverseOtherEvent : false;
                vm.predicateOtherEvent = predicate;
                vm.otherEvents = orderBy(vm.otherEvents, predicate, vm.reverseOtherEvent);
            };

        });
})();
