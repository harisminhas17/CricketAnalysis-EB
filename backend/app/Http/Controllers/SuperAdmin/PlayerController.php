<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use App\Models\SuperAdmin;
use App\Models\Player;
use App\HelperFunctions\HelperFunctions;

class PlayerController extends Controller
{
    //------------------ Players -----------------

    public function deletePlayer(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'player_ID' => 'required',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'error'   => true,
                'message' => 'Validation failed',
                'records' => $validator->errors()
            ], 422);
        }

        $player = Player::findOrFail($request->player_ID);
        $player->delete();

        return response()->json([
            'error'   => false,
            'message' => 'Player deleted successfully ' . $request->player_ID,
        ]);
    }
//------------------Edit Player---------------------
    public function editPlayers(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'player_ID'    => 'required',
            'user_name'    => 'sometimes',
            'email'        => 'sometimes',
            'password'     => 'sometimes',
            'phone_number' => 'sometimes',
            'sport_type'   => 'sometimes',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'error'   => true,
                'message' => 'Validation failed',
                'records' => $validator->errors()
            ], 422);
        }

        $player = Player::find($request->player_ID);

        if ($request->filled('password')) {
            $request->merge(['password' => Hash::make($request->password)]);
        }

        $player->update($request->only([
            'user_name',
            'email',
            'password',
            'phone_number',
            'sport_type'
        ]));

        return response()->json([
            'error'   => false,
            'message' => 'Player updated successfully',
            'records' => $player
        ], 200);
    }
}
