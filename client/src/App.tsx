import { useState, useEffect } from "react";
import "./App.css";

type Person = { clothes: string };
type Vehicle = { type: string; color: string; model: string };
type Scene = { persons: Person[]; vehicles: Vehicle[] };

function SceneCard({ scene }: { scene: Scene }) {
  return (
    <>
      <div className="scene-card">
        <div className="scene-card-title">Scene contents:</div>
        <div className="scene-card-content">
          <strong>People: </strong>
          {scene.persons.length}
          <div>
            {scene.persons.length > 0 &&
              scene.persons.map((person, i) => (
                <div key={i} className="scene-card-person">
                  <div> clothes: {person.clothes}</div>
                </div>
              ))}
          </div>
        </div>
        <div className="scene-card-content">
          <strong>Vehicles: </strong>
          {scene.vehicles.length}
          <div>
            {scene.vehicles.length > 0 &&
              scene.vehicles.map((vehicle, i) => (
                <div key={i} className="scene-card-vehicle">
                  <div> Type: {vehicle.type} </div>
                  <div> Model: {vehicle.model} </div>
                  <div> Color: {vehicle.color} </div>
                </div>
              ))}
          </div>
        </div>
      </div>
    </>
  );
}

function SceneLog({ scenes }: { scenes: Scene[] }) {
  return (
    <>
      <div className="scene-log">
        {scenes.map((scene, i) => {
          return <SceneCard key={i} scene={scene} />;
        })}
      </div>
    </>
  );
}

function App() {
  const [scenes, setScenes] = useState<Scene[]>([]);

  const getLatestScene = async () => {
    console.log("Getting latest scene...");
    const response = await fetch("http://localhost:5173/scene");
    const jsonResponse = await response.json();
    const newScene = jsonResponse.data;
    console.log(newScene);
    setScenes((scenes) => [newScene, ...scenes]);
  };

  // useEffect runs a function every time that a set of dependencies changes
  // if we pass deps: [] it means the function will be called only once (when mounting the component)
  useEffect(() => {
    // setInterval calls a function repeatedly with a time delay
    // it returns an interval ID that uniquely identifies that interval
    const interval = setInterval(getLatestScene, 10000);
    // clearInterval can be called using the interval ID to cancel the interval
    // useEffect should return a callback to be invoked as cleanup
    return () => clearInterval(interval);
    // Note: in development mode, react will run in StrictMode which will try to simulate
    // the behaviour of mounting and unmounting and remounting a component to uncover bugs.
    // This means that unless you have clearInterval you'll get two getLatestScene calls
    // at the same time!
  }, []);

  return (
    <>
      <h1>CCTV Logger</h1>
      <div className="card">
        <button className="button" onClick={getLatestScene}>
          Get log
        </button>
        <br />
        <SceneLog scenes={scenes} />
      </div>
    </>
  );
}

export default App;
