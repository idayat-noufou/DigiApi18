import http from "k6/http";
import { sleep } from "k6";

export let options = {
  stages: [
    { duration: "30s", target: 10 },   // montée à 10 utilisateurs
    { duration: "30s", target: 50 },   // montée à 50 utilisateurs
    { duration: "30s", target: 100 },  // montée à 100 utilisateurs
    { duration: "30s", target: 0 },    // retour à 0
  ],
};

export default function () {
  http.get("http://localhost:8000/");
  http.get("http://localhost:8000/api/v1/client");

  http.post(
    "http://localhost:8000/api/v1/client",
    JSON.stringify({
      nom: "Test",
      prenom: "Load",
      adresse: "Rue k6",
    }),
    { headers: { "Content-Type": "application/json" } }
  );

  sleep(1);
}
