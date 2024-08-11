import { useState, useEffect } from "react";
import "./App.css";

type Person = { clothes: string; gender: "male" | "female" | "unsure" };
type Vehicle = { type: string; color: string };
type Environment = { weather: string; summary: string };
type Scene = {
  persons: Person[];
  vehicles: Vehicle[];
  environment: Environment;
};
type SceneData = {
  scene: Scene;
  timestamp: string;
};

function capitalizeFirstLetter(text: string) {
  return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
}

function SceneCard({
  sceneData,
  visible,
}: {
  sceneData: SceneData;
  visible: boolean;
}) {
  const scene = sceneData.scene;
  const timestamp = new Date(sceneData.timestamp);

  return (
    <>
      <div className={`scene-card ${visible ? "visible" : ""}`}>
        <div className="scene-card-timestamp">
          {timestamp.toLocaleDateString("en-GB", {
            hour: "numeric",
            minute: "numeric",
            second: "numeric",
          })}
        </div>
        <div className="scene-card-title">Scene description:</div>
        <div className="scene-card-environment">
          <strong>🌦️ Environment: </strong>
          <div>
            <div className="scene-card-summary">
              {scene.environment.summary}
            </div>
            <div className="scene-card-weather">
              Weather: {scene.environment.weather}
            </div>
          </div>
        </div>
        <div className="scene-card-contents">
          <div className="scene-card-people">
            <strong>🧍 People: </strong>
            {scene.persons.length}
            <div>
              {scene.persons.length > 0 &&
                scene.persons.map((person, i) => (
                  <div key={i} className="scene-card-person">
                    <div> Clothes: {capitalizeFirstLetter(person.clothes)}</div>
                    <div>
                      {" "}
                      {person.gender != "unsure" &&
                        `Gender: ${capitalizeFirstLetter(person.gender)}`}
                    </div>
                  </div>
                ))}
            </div>
          </div>
          <div className="scene-card-content">
            <strong>🚗 Vehicles: </strong>
            {scene.vehicles.length}
            <div>
              {scene.vehicles.length > 0 &&
                scene.vehicles.map((vehicle, i) => (
                  <div key={i} className="scene-card-vehicle">
                    <div> Type: {capitalizeFirstLetter(vehicle.type)} </div>
                    <div> Color: {capitalizeFirstLetter(vehicle.color)} </div>
                  </div>
                ))}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

function App() {
  const [sceneData, setSceneData] = useState<SceneData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [visible, setVisible] = useState<boolean>(false);

  const getLatestScene = async () => {
    setIsLoading(true);
    console.log("Getting latest scene...");
    let newSceneData = null;

    try {
      const response = await fetch("http://localhost:5173/scene");
      const jsonResponse = await response.json();
      newSceneData = jsonResponse.scene_data;
      console.log(newSceneData);
    } catch (error) {
      console.error("Error fetching scene: ", error);
    } finally {
      setIsLoading(false);
      setVisible(false);
      setSceneData(newSceneData);
      setTimeout(() => setVisible(true), 400);
    }
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
      <div className="header">
        <h1>CCTV Logger</h1>
        <button className="button" onClick={getLatestScene}>
          {isLoading ? (
            <i className="fas fa-spinner fa-spin" />
          ) : (
            <i className="fas fa-sync-alt" />
          )}
        </button>
      </div>
      <br />
      {sceneData && <SceneCard sceneData={sceneData} visible={visible} />}
    </>
  );
}

export default App;
