# Little Wilds

A small first-person voxel building game. It uses the browser's built-in WebGL support and Python's standard library; no packages are required.

## Start the game

On Windows, double-click `run_game.bat`. It starts the local game server and opens the game in your default browser. Keep the server window open while playing. Press Ctrl+C in that window to stop it.

## Controls

- Click **Enter Fernhaven**, then use **W A S D** to move and the mouse to look.
- **Space** jumps; **Shift** moves slowly.
- Aim at a block and **hold left-click** to break it. Blocks drop as floating items.
- Aim beside a block and **right-click** to place the selected block.
- Walk close to a floating item to pick it up. The hotbar only shows blocks you have collected.
- Press **Q** to drop one selected block and **E** to craft a crafting table from four timber blocks.
- Sand blocks fall until they reach a solid block. Leaves are non-solid so you can walk under trees.
- Select a hotbar slot with **1–9** or click it. Press **Esc** to pause, then click the world to return.

## Add mods

The local launcher reads `Modifications/manifest.json` and then reads `mod.json` inside each folder listed in `ModFolders`.

```json
{
  "ModFolders": {
    "SuperMarioModFolderName": "SuperMario"
  }
}
```

The key is the mod's internal name; the value is the folder name inside `Modifications`. Add a `mod.json` in that folder:

```json
{
  "Name": "My Blocks",
  "Blocks": [
    { "Id": "crystal", "Name": "Crystal", "Color": "#78d8ed", "StartingCount": 12 }
  ]
}
```

Each block needs a unique `Id`, a display `Name`, and a six-digit hex `Color`. `StartingCount` is optional and defaults to 12. Mods add blocks to the hotbar and provide their starting inventory. The included `Modifications/SuperMario/mod.json` is a working example.
