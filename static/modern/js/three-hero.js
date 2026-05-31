(()=>{
  // Lightweight Three.js hero scene: floating simple objects
  function initHero(){
    const container = document.querySelector('.three-hero');
    if(!container) return;

    const width = container.clientWidth;
    const height = container.clientHeight;

    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0xf7fbff, 0.0025);

    const camera = new THREE.PerspectiveCamera(35, width/height, 0.1, 1000);
    camera.position.set(0, 0, 45);

    const renderer = new THREE.WebGLRenderer({antialias:true,alpha:true});
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(width, height);
    renderer.outputEncoding = THREE.sRGBEncoding;
    container.appendChild(renderer.domElement);

    // Lights
    const hemi = new THREE.HemisphereLight(0xffffff, 0xddddff, 0.8);
    scene.add(hemi);
    const dir = new THREE.DirectionalLight(0xffffff, 0.6);
    dir.position.set(10,20,10);
    scene.add(dir);

    // Simple low-poly objects to represent items
    const group = new THREE.Group();

    const materialA = new THREE.MeshStandardMaterial({color:0x2563EB,metalness:0.3,roughness:0.4});
    const materialB = new THREE.MeshStandardMaterial({color:0x0EA5E9,metalness:0.2,roughness:0.5});
    const materialC = new THREE.MeshStandardMaterial({color:0xF59E0B,metalness:0.1,roughness:0.6});

    function makeItem(geom, mat, x,y,z,scale){
      const m = new THREE.Mesh(geom, mat);
      m.position.set(x,y,z);
      m.scale.setScalar(scale||1);
      m.castShadow = true;
      m.receiveShadow = true;
      group.add(m);
      return m;
    }

    // wallet-like box
    makeItem(new THREE.BoxGeometry(6,3.5,0.8), materialA, -12, 0, 0, 1.0);
    // phone-like thin box
    makeItem(new THREE.BoxGeometry(3.2,6,0.4), materialB, -4, 6, -2, 0.9);
    // keys approximated as torus
    makeItem(new THREE.TorusGeometry(1.2,0.35,16,60), materialC, 6, -2, 2, 1.1);
    // backpack as rounded box
    makeItem(new THREE.BoxGeometry(5,6,2.4), materialA, 10, 4, -4, 1.0);
    // id card as plane
    const idGeom = new THREE.PlaneGeometry(4,2.5);
    makeItem(idGeom, materialB, 2, -6, -1, 1.0);
    // headphones as torus pair
    makeItem(new THREE.TorusGeometry(2.2,0.35,16,60), materialC, -8, -4, 3, 0.9);

    scene.add(group);

    // subtle float animation params
    const floats = [];
    group.children.forEach((c,i)=>{
      floats.push({mesh:c, speed:0.2+Math.random()*0.5, offset:Math.random()*Math.PI*2, rotSpeed:0.002+Math.random()*0.006});
    });

    // parallax on mouse
    const mouse = {x:0,y:0};
    window.addEventListener('mousemove', (e)=>{
      const rect = container.getBoundingClientRect();
      mouse.x = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
      mouse.y = ((e.clientY - rect.top) / rect.height - 0.5) * -2;
    });

    function onResize(){
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w/h;
      camera.updateProjectionMatrix();
      renderer.setSize(w,h);
    }
    window.addEventListener('resize', onResize);

    let t=0;
    function animate(){
      t += 0.016;
      // float
      floats.forEach(f=>{
        f.mesh.position.y += Math.sin(t * f.speed + f.offset) * 0.02;
        f.mesh.rotation.y += f.rotSpeed;
        f.mesh.rotation.x += f.rotSpeed/2;
      });

      // camera gentle parallax
      camera.position.x += (mouse.x*6 - camera.position.x) * 0.05;
      camera.position.y += (mouse.y*3 - camera.position.y) * 0.05;
      camera.lookAt(0,0,0);

      renderer.render(scene, camera);
      requestAnimationFrame(animate);
    }

    // initial render
    animate();
  }

  // run when DOM ready
  document.addEventListener('DOMContentLoaded', initHero);
})();
