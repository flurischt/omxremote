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

    // load a list of movie-filenames from server
    $scope.movies = [];
    $http.get('/api/list').
        success(function(data, status, headers, config) {
            $.each(data, function(i) {
                m = data[i];
                $scope.movies.push({'filename' : m.filename, 'hash' : m.hash}); 
            });
        }).
        error(function(data, status, headers, config) {
        });

    $scope.togglePlay = function() {
        status = (++status) % 2;
        $scope.playPauseText = playPauseText[status]; 
        $scope.playPauseClass = playPauseIcon[status];
        // pause can be used to toggle play/pause
        $scope.sendCommand('pause');
    }

    $scope.sendCommand = function(cmd) {
        $http.post('/api/exec/' + cmd, {}).
          success(function(data, status, headers, config) {
            $scope.updateStatus();
          }).
          error(function(data, status, headers, config) {
            //TODO
          });
    }

    $scope.changeMovie = function() {
        if(!$scope.selectedMovie)
            return;

        var modalInstance = $modal.open({
          animation: true,
          templateUrl: 'modal.html',
          controller: 'ModalInstanceCtrl',
        });

        modalInstance.result.then(function () {
            $http({
                method: 'POST',
                url: '/api/changeMovie',
                data: $.param({hash : $scope.selectedMovie.hash}),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).
                success(function(data, status, headers, config) {
                    $scope.updateStatus();
                }).
                error(function(data, status, headers, config) {
                    //TODO
                });
            }, function () {
                //DO NOTHING (aka continue playback)
        });
    }

	$scope.updateStatus = function() {
        $http.get('/api/status').
            success(function(data, status, headers, config) {
                $scope.filename = data.filename; 
                $scope.position = data.progress;
                $scope.duration = data.duration;
                //$scope.position = (new Date)
                //    .setSeconds(data.progress)
                //    .toString('H:mm:ss');
                //$scope.duration = (new Date)
                //    .setSeconds(data.duration)
                //    .toString('H:mm:ss');
                if(data.playback) {
                    status = 1;
                    //TODO let angular handler the text-changes. 
                    // just update status here...
                    $scope.playPauseText = playPauseText[status]; 
                    $scope.playPauseClass = playPauseIcon[status];
                }
            }).
            error(function(data, status, headers, config) {
                //TODO remove / doublecheck
                alert('fail');
            });
    }

	// TODO: enable, refresh progress every 30 seconds
    $interval($scope.updateStatus, 1e4);
    $scope.updateStatus();
});

