var PringleCurve = THREE.Curve.create(

	function(radius) {
		this.radius = radius; 
	},

	function(t) {
		var time = t;

		var tx = this.radius * Math.cos(time*Math.PI*2);
		var ty = Math.sin(time*Math.PI*4) * this.radius/2;
		var tz = this.radius * Math.sin(time*Math.PI*2);

		return new THREE.Vector3(tx, ty, tz);
	}
);

var Pringles = function(){

	var object3D = new THREE.Object3D();
	var radius = 140;
	var numMeshes = 6;

	var speed = 2;
	var controls = {
		xSpeed: speed,
		ySpeed: 0,
		zSpeed: 0,
	};

	function init(){

		var knot = new PringleCurve(radius);

		var segments = 100;
		var radiusSegments = 2;
		var thickness = 4.0;
		var tube = new THREE.TubeGeometry(knot, segments, thickness, radiusSegments, true);

		var mat = new THREE.MeshBasicMaterial({
			color: 0xFFAA33,
			blending: THREE.AdditiveBlending,
			transparent: true,
			opacity: 0.2,
			depthTest: false
		});
		var mat2 = new THREE.MeshBasicMaterial({
			color: 0xFFAA33,
			blending: THREE.AdditiveBlending,
			transparent: true,
			opacity: 0.5,
			depthTest: false
		});

		for (var i = numMeshes - 1; i >= 0; i--) {
			var _mat = (i % 2=== 0) ? mat : mat2;
			var tubeMesh = new THREE.Mesh( tube, _mat );
			object3D.add(tubeMesh);
		}
	}

	var frame = 0;
	function update(){

		var halfMeshLen = object3D.children.length * 0.5;
		object3D.children.forEach(function(mesh, i){
			i=i+speed*numMeshes*2;

			var multiplier = (i % 2 === 0) ? 1 : -1;
			mesh.rotation.x += (i-halfMeshLen) * controls.xSpeed * 0.0001 * multiplier;
			mesh.rotation.y += (i-halfMeshLen) * controls.ySpeed * 0.0001;
			mesh.rotation.z += controls.zSpeed * 0.001;

		});

		frame ++;
	}

	init();

	_.extend(this, {
		object3D: object3D,
		update: update
	});

};


// three.js scene
//var camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 20000 );
//camera.position.set( 0, 0, 300 );
var camera = new THREE.OrthographicCamera( window.innerWidth / - 2, window.innerWidth / 2, window.innerHeight / 2, window.innerHeight / - 2, - 500, 1000 );

var scene = new THREE.Scene();
var renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
renderer.setPixelRatio(devicePixelRatio);
document.body.appendChild( renderer.domElement );

var pringles = new Pringles();
scene.add(pringles.object3D);

function update(){
  requestAnimationFrame( update );
  renderer.render(scene, camera);
  pringles.update();
}
update();

window.addEventListener('resize', function(){
  renderer.setSize( window.innerWidth, window.innerHeight );
  camera.left = window.innerWidth / - 2;
  camera.right = window.innerWidth / 2;
  camera.top = window.innerHeight / 2;
  camera.bottom = window.innerHeight / - 2;
  camera.updateProjectionMatrix();
});