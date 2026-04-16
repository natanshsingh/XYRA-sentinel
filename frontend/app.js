import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// --- THREE.JS SCENE SETUP ---
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x050510, 0.002);

const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 30, 80);

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
container.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.5;

// Grid Helper for base
const gridHelper = new THREE.GridHelper(200, 100, 0x00f0ff, 0x112244);
gridHelper.position.y = -10;
scene.add(gridHelper);

// Decorative particles
const particlesGeometry = new THREE.BufferGeometry();
const particlesCount = 1000;
const posArray = new Float32Array(particlesCount * 3);

for(let i = 0; i < particlesCount * 3; i++) {
    posArray[i] = (Math.random() - 0.5) * 200;
}
particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
const particlesMaterial = new THREE.PointsMaterial({
    size: 0.5,
    color: 0x00f0ff,
    transparent: true,
    opacity: 0.5,
    blending: THREE.AdditiveBlending
});
const particleMesh = new THREE.Points(particlesGeometry, particlesMaterial);
scene.add(particleMesh);

// Center core sphere
const coreGeometry = new THREE.IcosahedronGeometry(10, 2);
const coreMaterial = new THREE.MeshBasicMaterial({ 
    color: 0x00f0ff, 
    wireframe: true, 
    transparent: true, 
    opacity: 0.3 
});
const coreMesh = new THREE.Mesh(coreGeometry, coreMaterial);
scene.add(coreMesh);

const innerGeometry = new THREE.IcosahedronGeometry(7, 1);
const innerMaterial = new THREE.MeshBasicMaterial({ color: 0x00aaff, transparent: true, opacity: 0.8 });
const innerMesh = new THREE.Mesh(innerGeometry, innerMaterial);
scene.add(innerMesh);

// Ambient Light
const ambientLight = new THREE.AmbientLight(0x404040);
scene.add(ambientLight);

// Interactive Mouse Light & Raycasting
const mouseLight = new THREE.PointLight(0xffffff, 5, 80);
scene.add(mouseLight);

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

// Invisible plane for smooth raycaster intersection capturing
const planeGeometry = new THREE.PlaneGeometry(1000, 1000);
const planeMaterial = new THREE.MeshBasicMaterial({ visible: false });
const intersectPlane = new THREE.Mesh(planeGeometry, planeMaterial);
scene.add(intersectPlane);

window.addEventListener('mousemove', (event) => {
    // Calculate mouse position in normalized device coordinates (-1 to +1)
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObject(intersectPlane);
    if (intersects.length > 0) {
        // Light follows mouse
        mouseLight.position.copy(intersects[0].point);
        mouseLight.position.z = 5; 
        
        // Dynamically scale core if mouse gets near
        const distToCore = coreMesh.position.distanceTo(intersects[0].point);
        if (distToCore < 25) {
            coreMesh.scale.lerp(new THREE.Vector3(1.3, 1.3, 1.3), 0.1);
            innerMesh.scale.lerp(new THREE.Vector3(1.2, 1.2, 1.2), 0.1);
        } else {
            coreMesh.scale.lerp(new THREE.Vector3(1, 1, 1), 0.1);
            innerMesh.scale.lerp(new THREE.Vector3(1, 1, 1), 0.1);
        }
    }
});

// Click interaction
window.addEventListener('click', () => {
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObject(coreMesh);
    if (intersects.length > 0) {
        addLog("[USER ACTION] System core pinged manually. Status: Verified.");
        
        const flashLight = new THREE.PointLight(0xffffff, 20, 100);
        scene.add(flashLight);
        setTimeout(() => scene.remove(flashLight), 200);
        
        // Give the grid a little interactive bounce
        gridHelper.position.y = -5;
        setTimeout(() => gridHelper.position.y = -10, 150);
    }
});


window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// --- ANIMATION LOOP ---
const clock = new THREE.Clock();
function animate() {
    requestAnimationFrame(animate);
    
    const elapsedTime = clock.getElapsedTime();
    coreMesh.rotation.y += 0.005;
    coreMesh.rotation.x += 0.002;
    innerMesh.rotation.y -= 0.01;
    
    particleMesh.rotation.y = elapsedTime * 0.05;
    
    controls.update();
    renderer.render(scene, camera);
}
animate();

// --- DATA FETCHING & UI UPDATE ---
const valPeople = document.getElementById('val-people');
const valScore = document.getElementById('val-score');
const riskLevelText = document.getElementById('risk-level-text');
const meterPath = document.getElementById('meter-path');
const threatStatus = document.getElementById('threat-status');
const logStream = document.getElementById('log-stream');
const cameraFeed = document.getElementById('camera-feed');

// Add a log entry
function addLog(message, isThreat = false) {
    const entry = document.createElement('div');
    entry.className = `log-entry ${isThreat ? 'threat' : ''}`;
    const timestamp = new Date().toLocaleTimeString();
    entry.innerText = `[${timestamp}] ${message}`;
    logStream.appendChild(entry);
    
    // Auto scroll bottom
    logStream.scrollTop = logStream.scrollHeight;
    
    // keep max 50 logs
    if (logStream.children.length > 50) {
        logStream.removeChild(logStream.firstChild);
    }
}

// Variables tracking state
let currentRisk = 'LOW';
let previousNumPeople = -1;

async function fetchMetrics() {
    try {
        const response = await fetch('/api/metrics');
        if (!response.ok) return;
        const data = await response.json();
        
        // Update DOM
        valPeople.innerText = data.num_people;
        valScore.innerText = parseFloat(data.score).toFixed(2);
        riskLevelText.innerText = data.risk_level;
        
        // Log if people count changed
        if (previousNumPeople !== -1 && data.num_people !== previousNumPeople) {
            addLog(`Tracking update: ${data.num_people} target(s) identified.`);
        }
        previousNumPeople = data.num_people;
        
        // Risk meter SVG logic (125 is empty, 0 is full)
        const scoreVal = parseFloat(data.score);
        meterPath.style.strokeDashoffset = 125 - (125 * Math.min(scoreVal, 1.0));
        
        // Visual updates based on Risk Level
        if (data.risk_level === 'HIGH') {
            meterPath.style.stroke = '#ff3366';
            riskLevelText.style.color = '#ff3366';
            riskLevelText.style.textShadow = '0 0 10px rgba(255,51,102,0.5)';
            
            threatStatus.innerText = '⚠️ THREAT DETECTED ⚠️';
            threatStatus.className = 'status-text target-threat';
            
            // 3D effects
            coreMaterial.color.setHex(0xff3366);
            innerMaterial.color.setHex(0xff0000);
            gridHelper.material.color.setHex(0xff3366);
            
            if (currentRisk !== 'HIGH') {
                addLog('CRITICAL: High risk behavior pattern detected!', true);
            }
        } else if (data.risk_level === 'MEDIUM') {
            meterPath.style.stroke = '#ffaa00';
            riskLevelText.style.color = '#ffaa00';
            riskLevelText.style.textShadow = '0 0 10px rgba(255,170,0,0.5)';
            
            threatStatus.innerText = 'ELEVATED SUSPICION';
            threatStatus.className = 'status-text target-normal';
            threatStatus.style.color = '#ffaa00';
            threatStatus.style.border = '1px solid rgba(255, 170, 0, 0.3)';
            
            coreMaterial.color.setHex(0xffaa00);
            innerMaterial.color.setHex(0xdd8800);
            gridHelper.material.color.setHex(0xffaa00);
        } else {
            meterPath.style.stroke = '#00f0ff';
            riskLevelText.style.color = '#00f0ff';
            riskLevelText.style.textShadow = '0 0 10px rgba(0,240,255,0.5)';
            
            threatStatus.innerText = 'Monitoring Normal';
            threatStatus.className = 'status-text target-normal';
            threatStatus.style.color = '';
            threatStatus.style.border = '';
            
            // Revert 3D styles
            coreMaterial.color.setHex(0x00f0ff);
            innerMaterial.color.setHex(0x00aaff);
            gridHelper.material.color.setHex(0x00f0ff);
        }
        
        currentRisk = data.risk_level;
        
    } catch (err) {
        console.error("Error fetching metrics:", err);
    }
}

// Fetch metrics every second
setInterval(fetchMetrics, 1000);
