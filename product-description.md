# Product Description: FPS Bot Arena with "The Glitch"

## Overview
A First-Person Shooter (FPS) game where the player fights against waves of tactical AI bots in a multi-room indoor facility. The core loop involves combat, earning money from kills, and upgrading weapons. The game features a meta-twist ending where the final weapon, an RPG, triggers a simulated game crash (Fake BSOD/Error) upon use.

## Gameplay Mechanics
*   **Perspective:** First-Person.
*   **Controls:** Standard FPS controls (WASD + Mouse).
*   **Interaction:** Pressing 'B' opens a real-time inventory/shop wheel to buy and switch weapons.
*   **Win/Loss:**
    *   **Loss:** Player health reaches zero.
    *   **"Win":** Acquiring and firing the final RPG, triggering the "crash" ending.

## Economy & Progression
*   **Income:** Bots drop money as physical items upon death, which the player must collect.
*   **Weapon Progression:**
    1.  **Pistol:** Starting weapon.
    2.  **Shotgun:** High close-range damage.
    3.  **Assault Rifle:** Rapid fire, medium range.
    4.  **RPG (Final Weapon):** Expensive endgame item. Firing it causes a fake "Blue Screen of Death" or critical error message, effectively ending the session.

## AI & Enemies
*   **Behavior:** Bots exhibit tactical behavior, utilizing the environment for cover and attempting flanking maneuvers rather than rushing blindly.

## Visuals & Environment
*   **Style:** Prototype aesthetic using simple geometric primitives (cubes, spheres) to represent characters, weapons, and the world.
*   **Setting:** A multi-room indoor facility designed with obstacles for cover and navigation.
*   **HUD:** Standard display showing Health Bar, Current Ammo, and Money Balance.

## Technical Strategy
*   **Platform:** Easiest path to implementation (likely Web/HTML5 + Three.js or Python + PyGame/Ursina) to avoid heavy resource requirements.
*   **Assets:** Procedural or basic geometric shapes; no external art assets required.
