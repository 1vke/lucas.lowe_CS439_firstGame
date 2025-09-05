# First Game GDD
**Class:** CS439 Game Engine Development | **Author:** Lucas Lowe

## 1. Game Overview
The game is a straightforward, **arcade-style point-and-click target shooter** with a nostalgic, late 2000s aesthetic. The primary goal is to achieve the highest score possible by accurately clicking on targets as they appear on the screen.

The game flows through a series of timed rounds. During each round, targets appear at various locations. The challenge lies in the player's speed and precision. The game operates on a continuous loop:
1.  The player starts at the **Start Screen**.
2.  Pressing "Play" begins the **Gameplay Session**.
3.  When the final round's timer ends, the session concludes.
4.  The game returns to the **Start Screen**, displaying the final score from the session that just ended.

---

## 2. Game Architecture

* **Scene Management**: The game will be built around a single `MainScene` class. This scene manages different **game states** (`START`, `PLAYING`) internally. This approach is efficient as all visual assets and objects can be loaded once and persist through the game loop.
* **Game States**:
    * `START`: The initial state. It displays the game title, the start/play again button, and the score from the previous session.
    * `PLAYING`: The active gameplay state. The timer is running, targets are active, and the score is being updated.

---

## 3. Sprite and GUI Details

#### Sprites
A fixed pool of **10-15 target sprites** will be created and stored in a list when the game starts. Instead of being destroyed, they are "recycled" by moving them on and off the screen, which is highly efficient.

* **Target Sprite**
    * **Visuals**: A visually clear object that fits the tropical theme, such as a stylized **red-and-white bullseye**, a coconut, or a pineapple.
    * **Animation**: A simple "pop-up" scale animation when it appears on screen.
    * **Life Span**: A target becomes active when moved onto the screen. It is deactivated in one of two ways: 1) the player successfully clicks it, or 2) its individual 3-second timer expires.
    * **Behavior**: The target is static once it appears. On a successful click (collision), it is immediately moved back to its off-screen position.

#### GUI Elements
All UI elements will be created during initialization, with their visibility toggled based on the game state.

* **Title / Game Over Label**
    * **Purpose**: To display the game's title on the start screen.
    * **Appearance**: Large, bold, retro-styled text centered on the screen.
    * **Behavior**: Visible only in the `START` state.
* **Start / Retry Button**
    * **Purpose**: To start a new game session from the start screen.
    * **Appearance**: A clickable button with text like "Start Game" or "Play Again."
    * **Behavior**: Visible only in the `START` state. Clicking it resets the score/timer and switches the game state to `PLAYING`.
* **Score Label**
    * **Purpose**: To display the player's current score in real-time.
    * **Appearance**: Simple text in the top-left corner, e.g., "Score: 0".
    * **Behavior**: Visible only in the `PLAYING` state. Updates instantly when a target is hit.
* **Round & Timer Label**
    * **Purpose**: To show the current round and time remaining.
    * **Appearance**: Simple text in the top-right corner, e.g., "Time: 15 Round: 1".
    * **Behavior**: Visible only in the `PLAYING` state. The timer counts down each second.
* **Final Score Label**
    * **Purpose**: To display the score from the last-played game.
    * **Appearance**: Text displayed on the start screen, e.g., "Last Score: 1250".
    * **Behavior**: Visible only in the `START` state after one game has been completed.

---

## 4. Asset List
This is the list of required external files for the game.

* **Images**
    * `background_tropical.png`: A vibrant, retro-styled tropical background.
    * `target.png`: The graphic for the target sprite.
* **Sound Effects** 🔊
    * `target_hit.wav`: A satisfying "pop" sound for hitting a target.

---

## 5. Milestones
This plan is broken into runnable steps, each corresponding to a major git commit.

1.  **Project Setup & Background Display**:
    * Create the main game window and the `MainScene` class. Load and display the static background image.
    * **Result**: A runnable program showing the game's background.
2.  **Start Screen Implementation**:
    * Create and display the `TitleLabel`, `StartButton`, and `FinalScoreLabel`. Implement the `START` state logic to show these elements.
    * **Result**: A runnable program displaying a static start screen.
3.  **Gameplay State Transition**:
    * Make the `StartButton` functional. When clicked, it should hide the start screen UI, show the gameplay UI (`ScoreLabel`, `TimerLabel`), and switch the state to `PLAYING`.
    * **Result**: A runnable program where you can click "Start" to transition to a blank gameplay screen.
4.  **Target Spawning & Timer**:
    * In the `PLAYING` state, implement the main game timer that counts down. Create the logic to periodically move targets from their off-screen pool to random on-screen locations.
    * **Result**: A runnable game where targets appear and a timer counts down.
5.  **Core Interaction Loop**:
    * Implement click detection on targets. When a target is hit, move it off-screen, update the score, and play the hit sound. When the timer runs out, transition back to the `START` state, updating the final score.
    * **Result**: A complete and playable game loop.

The project will be considered **complete and submittable after Milestone 5**.

* **Stretch Goals**:
    * Implement a custom crosshair that replaces the system mouse cursor.
    * Add background music that fits the tropical theme.
    * Add the "pop-up" and "disappear" animations to the targets.