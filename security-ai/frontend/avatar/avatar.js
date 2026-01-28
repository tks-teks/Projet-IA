import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';

let state = 'idle';
let halo;
let head;
let mouth;
let alertIcon;

export function initAvatar(canvasId) {
  const canvas = document.getElementById(canvasId);
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, canvas.clientWidth / canvas.clientHeight, 0.1, 100);
  camera.position.set(0, 1.2, 4.5);

  const ambient = new THREE.AmbientLight(0x66ccff, 0.6);
  scene.add(ambient);
  const spot = new THREE.SpotLight(0x88aaff, 1.2);
  spot.position.set(2, 5, 3);
  scene.add(spot);

  const coreMaterial = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.6, roughness: 0.2 });
  head = new THREE.Mesh(new THREE.SphereGeometry(1, 32, 32), coreMaterial);
  scene.add(head);

  const visorMaterial = new THREE.MeshStandardMaterial({ color: 0x22d3ee, emissive: 0x0891b2, metalness: 0.2 });
  const visor = new THREE.Mesh(new THREE.TorusGeometry(0.7, 0.15, 16, 100), visorMaterial);
  visor.rotation.x = Math.PI / 2;
  visor.position.y = 0.1;
  scene.add(visor);

  halo = new THREE.Mesh(new THREE.TorusGeometry(1.4, 0.04, 16, 100), new THREE.MeshStandardMaterial({ color: 0x38bdf8 }));
  halo.rotation.x = Math.PI / 2;
  halo.position.y = 1.2;
  scene.add(halo);

  mouth = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.08, 0.1), new THREE.MeshStandardMaterial({ color: 0x7dd3fc, emissive: 0x38bdf8 }));
  mouth.position.y = -0.3;
  scene.add(mouth);

  alertIcon = new THREE.Mesh(new THREE.ConeGeometry(0.15, 0.3, 8), new THREE.MeshStandardMaterial({ color: 0xef4444 }));
  alertIcon.position.set(0, 1.8, 0);
  alertIcon.visible = false;
  scene.add(alertIcon);

  const clock = new THREE.Clock();

  function animate() {
    const t = clock.getElapsedTime();
    if (state === 'idle') {
      head.scale.y = 1 + Math.sin(t * 1.5) * 0.02;
      halo.material.color.setHex(0x38bdf8);
      halo.scale.setScalar(1 + Math.sin(t) * 0.02);
      mouth.scale.x = 1;
      alertIcon.visible = false;
    } else if (state === 'listening') {
      halo.material.color.setHex(0x22d3ee);
      halo.scale.setScalar(1 + Math.sin(t * 4) * 0.08);
      head.rotation.y = Math.sin(t * 2) * 0.1;
      alertIcon.visible = false;
    } else if (state === 'talking') {
      mouth.scale.x = 1 + Math.sin(t * 10) * 0.6;
      halo.material.color.setHex(0x7dd3fc);
      alertIcon.visible = false;
    } else if (state === 'alert') {
      halo.material.color.setHex(0xef4444);
      halo.scale.setScalar(1 + Math.sin(t * 6) * 0.12);
      head.rotation.x = Math.sin(t * 12) * 0.03;
      alertIcon.visible = true;
    }

    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }

  animate();

  window.addEventListener('resize', () => {
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
  });
}

export function setAvatarState(nextState) {
  state = nextState;
}
