angular.module("omxremote", ['ui.bootstrap']);

angular.module('omxremote').controller('ModalInstanceCtrl', function ($scope, $modalInstance) {
    $scope.ok = function () {
        $modalInstance.close();
    };
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});

angular.module("omxremote").controller("OmxRemoteCtrl", function ($scope, $modal, $interval, $http) {

    var playPauseIcon = ["glyphicon-play", "glyphicon-pause"];
    var playPauseText = ["Play", "Pause"];
    var status = 0; // 0=paused, 1=playing


    $scope.playPauseText = playPauseText[status]; 
    $scope.playPauseClass = playPauseIcon[status];

    $scope.filename = "";
    $scope.position = 0;
    $scope.duration = 0;
    $scope.selectedMovie = 0;

    $scope.movies = [
        {"filename" : "a.avi", "hash" : "asdf1"}, 
        {"filename" : "b.avi", "hash" : "asdf2"}, 
        {"filename" : "c.avi", "hash" : "asdf3"}
    ];

    $scope.togglePlay = function() {
        status = (++status) % 2;
        $scope.playPauseText = playPauseText[status]; 
        $scope.playPauseClass = playPauseIcon[status];
        // pause can be used to toggle play/pause
        $scope.sendCommand('pause');
    }

    $scope.sendCommand = function(cmd) {
        alert(cmd);
    }

    $scope.changeMovie = function() {
        var modalInstance = $modal.open({
          animation: true,
          templateUrl: 'modal.html',
          controller: 'ModalInstanceCtrl',
        });

        modalInstance.result.then(function () {
            alert('ok');
        }, function () {
            alert('cancel');
        });
    }

	$scope.updateStatus = function() {
        $http.get('/api/status').
            success(function(data, status, headers, config) {
            $scope.filename = data.filename; 
            $scope.position = data.progress; 
            $scope.duration = data.duration; 
            }).
            error(function(data, status, headers, config) {
                //TODO remove / doublecheck
                alert('fail');
            });
    }

	// TODO: enable, refresh progress every 30 seconds
    $interval($scope.updateStatus, 3e4);
});

