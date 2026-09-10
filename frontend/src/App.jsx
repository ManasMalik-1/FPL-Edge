import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function getPosition(positionId) {
  const positions = {
    1: "GK",
    2: "DEF",
    3: "MID",
    4: "FWD",
  };

  return positions[positionId] || "—";
}

function getDifficultyLabel(difficulty) {
  if (difficulty <= 2) return "Easy";
  if (difficulty === 3) return "Medium";
  return "Hard";
}

function App() {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [limit, setLimit] = useState(20);

  useEffect(() => {
    async function fetchRecommendations() {
      try {
        setLoading(true);

        const response = await fetch(
          `${API_URL}/recommendations?limit=${limit}`
        );

        if (!response.ok) {
          throw new Error(`API returned ${response.status}`);
        }

        const data = await response.json();
        setPlayers(data);
        setError(null);
      } catch (err) {
        console.error(err);
        setError("Could not connect to the FPL Edge API.");
      } finally {
        setLoading(false);
      }
    }

    fetchRecommendations();
  }, [limit]);

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>⚽ FPL Edge</h1>
          <p>Fantasy Premier League Decision Engine</p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          API Connected
        </div>
      </header>

      <main className="container">
        <section className="hero">
          <div>
            <span className="eyebrow">PLAYER RECOMMENDATIONS</span>

            <h2>Find your next FPL edge.</h2>

            <p>
              Players ranked using form, price, ownership and upcoming
              fixture difficulty.
            </p>
          </div>

          <div className="hero-stat">
            <strong>{players.length}</strong>
            <span>Players ranked</span>
          </div>
        </section>

        {loading && (
          <div className="message">
            Loading recommendations...
          </div>
        )}

        {error && (
          <div className="error">
            {error}
          </div>
        )}

        {!loading && !error && players.length > 0 && (
          <section className="recommendations">
            <div className="section-header">
              <div>
                <h3>Top Recommendations</h3>
                <p>
                  Highest scoring players from the current model.
                </p>
              </div>

              <select
                value={limit}
                onChange={(e) => setLimit(Number(e.target.value))}
              >
                <option value={10}>Top 10</option>
                <option value={20}>Top 20</option>
                <option value={50}>Top 50</option>
                <option value={100}>Top 100</option>
              </select>
            </div>

            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Player</th>
                    <th>Position</th>
                    <th>Price</th>
                    <th>Form</th>
                    <th>Ownership</th>
                    <th>Next GW</th>
                    <th>Opponent</th>
                    <th>Venue</th>
                    <th>Fixture</th>
                    <th>Avg Difficulty</th>
                    <th>Score</th>
                  </tr>
                </thead>

                <tbody>
                  {players.map((player, index) => (
                    <tr key={player.player_id}>
                      <td className="rank">
                        {index + 1}
                      </td>

                      <td className="player">
                        <strong>{player.player_name}</strong>
                      </td>

                      <td>
                        <span className="position">
                          {getPosition(player.position_id)}
                        </span>
                      </td>

                      <td>
                        £{Number(player.price).toFixed(1)}
                      </td>

                      <td className="form">
                        {Number(player.form).toFixed(1)}
                      </td>

                      <td>
                        {Number(
                          player.selected_by_percent
                        ).toFixed(1)}
                        %
                      </td>

                      <td className="gameweek">
                        GW{player.next_gameweek}
                      </td>

                      <td className="opponent">
                        <strong>
                          {player.next_opponent_short ||
                            player.next_opponent ||
                            "—"}
                        </strong>

                        {player.next_opponent && (
                          <span>
                            {player.next_opponent}
                          </span>
                        )}
                      </td>

                      <td>
                        <span
                          className={
                            player.venue === "Home"
                              ? "venue home"
                              : "venue away"
                          }
                        >
                          {player.venue}
                        </span>
                      </td>

                      <td>
                        <span
                          className={`difficulty difficulty-${player.next_fixture_difficulty}`}
                        >
                          {getDifficultyLabel(
                            player.next_fixture_difficulty
                          )}
                        </span>
                      </td>

                      <td>
                        {Number(
                          player.avg_fixture_difficulty
                        ).toFixed(2)}
                      </td>

                      <td>
                        <span className="score">
                          {Number(
                            player.recommendation_score
                          ).toFixed(2)}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}

        {!loading &&
          !error &&
          players.length === 0 && (
            <div className="message">
              No recommendations found.
            </div>
          )}
      </main>

      <footer>
        FPL Edge · Data-driven Fantasy Premier League analysis
      </footer>
    </div>
  );
}

export default App;