import * as THREE from './vendor/three.module.js';

export function createScene(container){
 const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
 let renderer;try{renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,powerPreference:'low-power'});}catch(e){document.querySelector('#fallback').hidden=false;return {update(){},view(){},zoom(){}};}
 renderer.setPixelRatio(Math.min(devicePixelRatio,1.7));container.prepend(renderer.domElement);
 const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(40,1,.1,100);
 let azimuth=.3,elevation=.22,distance=8.8,focus=new THREE.Vector3(),targetFocus=new THREE.Vector3(),view='mission';
 scene.add(new THREE.AmbientLight(0x829ab4,.38));const sunLight=new THREE.DirectionalLight(0xffefd5,2.2);sunLight.position.set(-6,3,5);scene.add(sunLight);
 function globeTexture(){
  const c=document.createElement('canvas');c.width=2048;c.height=1024;const ctx=c.getContext('2d');
  ctx.fillStyle='#123755';ctx.fillRect(0,0,c.width,c.height);
  const continents=[[-168,72,-130,72,-113,60,-94,52,-64,50,-55,43,-80,27,-98,16,-113,29,-128,49,-151,60],[-81,13,-59,8,-35,-7,-45,-22,-57,-40,-70,-55,-78,-24],[-17,35,9,38,34,31,51,12,44,-12,31,-35,18,-34,9,-15,-7,5],[-10,36,-10,60,21,71,64,72,107,76,150,61,180,66,157,47,135,34,116,21,107,1,97,13,78,7,68,27,48,30,37,44,15,42],[112,-12,139,-10,154,-25,146,-40,116,-33],[-52,60,-20,68,-26,82,-53,84,-67,73],[47,-13,51,-25,46,-27,43,-17],[129,31,143,44,145,36,136,31]];
  ctx.fillStyle='#496657';ctx.strokeStyle='#6a7e65';ctx.lineWidth=2;
  for(const shape of continents){ctx.beginPath();for(let i=0;i<shape.length;i+=2){let x=(shape[i]+180)/360*c.width,y=(90-shape[i+1])/180*c.height;i?ctx.lineTo(x,y):ctx.moveTo(x,y)}ctx.closePath();ctx.fill();ctx.stroke()}
  ctx.fillStyle='#c3cfd3';ctx.beginPath();ctx.moveTo(0,965);for(let x=0;x<=2048;x+=30)ctx.lineTo(x,948+Math.sin(x*.01)*18);ctx.lineTo(2048,1024);ctx.lineTo(0,1024);ctx.fill();
  // Seeded fine surface variation; approximate continents are intentionally schematic.
  let seed=412;const rnd=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296};
  for(let i=0;i<17000;i++){ctx.fillStyle=`rgba(180,205,197,${rnd()*.065})`;ctx.fillRect(rnd()*2048,rnd()*1024,1+rnd()*6,1+rnd()*4)}
  const texture=new THREE.CanvasTexture(c);texture.colorSpace=THREE.SRGBColorSpace;return texture;
 }
 const earth=new THREE.Mesh(new THREE.SphereGeometry(1.62,80,64),new THREE.MeshPhongMaterial({map:globeTexture(),specular:0x51798c,shininess:12}));earth.rotation.z=.14;scene.add(earth);
 const atmosphere=new THREE.Mesh(new THREE.SphereGeometry(1.67,64,48),new THREE.ShaderMaterial({transparent:true,side:THREE.BackSide,depthWrite:false,uniforms:{},vertexShader:'varying vec3 n;varying vec3 v;void main(){vec4 p=modelViewMatrix*vec4(position,1.0);n=normalize(normalMatrix*normal);v=normalize(-p.xyz);gl_Position=projectionMatrix*p;}',fragmentShader:'varying vec3 n;varying vec3 v;void main(){float rim=pow(1.0-abs(dot(normalize(n),normalize(v))),3.0);gl_FragColor=vec4(0.22,0.55,0.9,rim*0.65);}'}));scene.add(atmosphere);
 const orbitRadius=2.28,orbitPoints=[];function orbit(t){return new THREE.Vector3(Math.cos(t)*orbitRadius,Math.sin(t)*.68,Math.sin(t)*orbitRadius*.86)}
 for(let i=0;i<=200;i++)orbitPoints.push(orbit(i/200*Math.PI*2));
 scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(orbitPoints),new THREE.LineBasicMaterial({color:0x7196ae,transparent:true,opacity:.38})));
 const station=new THREE.Group(),metal=new THREE.MeshStandardMaterial({color:0xc9d1d6,metalness:.65,roughness:.4}),panel=new THREE.MeshStandardMaterial({color:0x71674a,metalness:.35,roughness:.65});
 function box(x,y,z,dx,dy,dz,material){const mesh=new THREE.Mesh(new THREE.BoxGeometry(dx,dy,dz),material);mesh.position.set(x,y,z);station.add(mesh);return mesh}
 box(0,0,0,.95,.045,.055,metal);box(0,0,0,.13,.12,.36,metal);box(.13,0,.11,.16,.09,.1,metal);box(-.12,0,.1,.15,.09,.1,metal);
 for(const x of [-.4,-.25,.25,.4])for(const sign of [-1,1]){box(x,0,sign*.22,.13,.012,.3,panel);for(let j=0;j<8;j++)box(x,.009,sign*.22-.14+j*.04,.131,.002,.002,metal)}
 const payload=new THREE.Mesh(new THREE.SphereGeometry(.025,12,12),new THREE.MeshBasicMaterial({color:0xd8eaaa}));payload.position.set(0,.07,.12);station.add(payload);scene.add(station);
 const stars=new Float32Array(2400);let seed=21;function random(){seed=(seed*16807)%2147483647;return(seed-1)/2147483646}for(let i=0;i<stars.length;i+=3){const a=random()*Math.PI*2,z=random()*2-1,r=25;stars[i]=Math.sqrt(1-z*z)*Math.cos(a)*r;stars[i+1]=z*r;stars[i+2]=Math.sqrt(1-z*z)*Math.sin(a)*r}
 scene.add(new THREE.Points(new THREE.BufferGeometry().setAttribute('position',new THREE.BufferAttribute(stars,3)),new THREE.PointsMaterial({color:0xa5b7c9,size:.027,transparent:true,opacity:.6})));
 const sun=new THREE.Mesh(new THREE.SphereGeometry(.11,24,20),new THREE.MeshBasicMaterial({color:0xffe9c0}));sun.position.set(-4.8,2.1,-2);scene.add(sun);
 const particles=new Float32Array(300*3);for(let i=0;i<particles.length;i++)particles[i]=(random()-.5)*7;
 const radiation=new THREE.Points(new THREE.BufferGeometry().setAttribute('position',new THREE.BufferAttribute(particles,3)),new THREE.PointsMaterial({color:0xe1b884,size:.018,transparent:true,opacity:.25}));scene.add(radiation);
 let progress=0,rate=null,p95=200,last=0,spin=0,drag=null;
 container.addEventListener('pointerdown',e=>{drag={x:e.clientX,y:e.clientY};container.setPointerCapture?.(e.pointerId)});
 container.addEventListener('pointermove',e=>{if(!drag)return;azimuth-=(e.clientX-drag.x)*.006;elevation=Math.max(-1,Math.min(1,elevation+(e.clientY-drag.y)*.004));drag={x:e.clientX,y:e.clientY}});
 window.addEventListener('pointerup',()=>drag=null);container.addEventListener('wheel',e=>{e.preventDefault();distance=Math.max(3.5,Math.min(13,distance+e.deltaY*.005))},{passive:false});
 const resize=()=>{const w=container.clientWidth,h=container.clientHeight;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix()};new ResizeObserver(resize).observe(container);resize();
 function animate(ms){requestAnimationFrame(animate);const dt=Math.min((ms-last)/1000,.05);last=ms;
  if(!reduced){spin+=dt*.018;earth.rotation.y=spin;}station.position.copy(orbit(progress*Math.PI*12+.45));station.rotation.y=-progress*Math.PI*12;station.rotation.z=.15;
  targetFocus.copy(view==='iss'?station.position:new THREE.Vector3());focus.lerp(targetFocus,.1);camera.position.set(focus.x+Math.sin(azimuth)*distance,focus.y+elevation*distance,focus.z+Math.cos(azimuth)*distance);camera.lookAt(focus);
  const activity=rate===null?0:Math.min(1,rate/Math.max(1,p95));radiation.geometry.setDrawRange(0,Math.round(activity*300));
  if(!reduced&&activity>0){for(let i=0;i<particles.length;i+=3){particles[i]+=dt*(.13+activity*.6);if(particles[i]>3.5)particles[i]=-3.5}radiation.geometry.attributes.position.needsUpdate=true}
  renderer.render(scene,camera);
 }requestAnimationFrame(animate);
 return {update(p,r,threshold){progress=p;rate=r;p95=threshold},view(v){view=v;distance=v==='iss'?3.5:v==='earth'?6.4:8.8;azimuth=.3;elevation=.22},zoom(amount){distance=Math.max(3.5,Math.min(13,distance+amount))}};
}
