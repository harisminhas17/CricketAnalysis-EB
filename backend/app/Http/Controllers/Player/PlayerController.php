<?php

namespace App\Http\Controllers\Player;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use App\Models\Player;
use App\HelperFunctions\HelperFunctions;

class PlayerController extends Controller
{

    public function addPlayer(Request $request)
    {

        $request->validate([
            'sport_type' => 'required',
            'name' => 'required',
            'email' => 'required',
            'phone' => 'nullable',
            'password' => 'required|min:6',
            'login_type' => 'required',
            'gender' => 'required|in:male,female,other',
            'date_of_birth' => 'required',
            'address' => 'required',
            'nationality_id' => 'required',
            'profile_image' => 'nullable',
            'role_id' => 'nullable|integer',
            'batting_style' => 'nullable',
            'bowling_style' => 'nullable',
            'dominant_hand' => 'nullable',
        ]);

        // Check if email already exists
        if (Player::where('email', $request->email)
            ->where('login_type', $request->login_type)
            ->where('sport_type', $request->sport_type)
            ->exists()
        ) {
            return response()->json([
                'error' => true,
                'message' => 'Player email already exists with ' . $request->login_type . ' for ' . $request->sport_type,
            ], 200);
        }

        // Check if phone number already exists
        if (Player::where('phone_number', $request->phone)->exists()) {
            return response()->json([
                'error' => true,
                'message' => 'Phone number ' . $request->phone . ' already exists',
            ], 200);
        }


        try {
            $imagePath = null;
            // Handle profile image upload
            if ($request->hasFile('profile_image')) {
                $imagePath = HelperFunctions::uploadImage($request->file('profile_image'), 'uploads/players/');
            }

            $player = Player::create([
                'sport_type' => $request->sport_type,
                'user_name' => $request->name,
                'email' => $request->email,
                'phone_number' => $request->phone,
                'password' => Hash::make($request->password),
                'login_type' => $request->login_type,
                'gender' => $request->gender,
                'date_of_birth' => date('Y-m-d', strtotime($request->date_of_birth)),
                'address' => $request->address,
                'nationality_id' => $request->nationality_id,
                'profile_image' => $imagePath,
                'player_role_id' => $request->role_id,
                'batting_style' => $request->batting_style,
                'bowling_style' => $request->bowling_style,
                'dominant_hand' => $request->dominant_hand,
                'created_at' => now(),
            ]);
        } catch (\Exception $e) {
            return response()->json([
                'message' => 'Error registering player',
                'error' => $e->getMessage()
            ], 200);
        }

        return response()->json([
            'error' => false,
            'message' => 'Player registered successfully' . ' with ' . $request->login_type . ' for ' . $request->sport_type,
            'records' => $player
        ]);
    }

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
            ], 200);
        }

        $player = Player::where('id', $request->player_ID)->first();

        $player->delete();

        return response()->json([
            'error'   => false,
            'message' => 'Player deleted successfully:' . $request->player_ID,
        ]);
    }

    public function getAllPlayers(Request $request)
    {
        $players = Player::all();

        if($players->isEmpty()) {
            return response()->json([
                'error'   => true,
                'message' => 'No players found',
            ], 200);
        }

        return response()->json([
            'error'   => false,
            'message' => 'All players fetched successfully',
            'records' => $players
        ]);
    }

    public function editPlayer(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'player_ID'    => 'required',
            'user_name'    => 'sometimes',
            'email'        => 'sometimes',
            'password'     => 'sometimes',
            'phone_number' => 'sometimes',
            'sport_type'   => 'sometimes',
            'address'      => 'sometimes',
            'date_of_birth' => 'sometimes',
            'gender'       => 'sometimes',
            'nationality_id' => 'sometimes',
            'profile_image' => 'sometimes',
            'player_role_id' => 'sometimes',
            'batting_style' => 'sometimes',
            'bowling_style' => 'sometimes',
            'dominant_hand' => 'sometimes',
            'city'         => 'sometimes',
            'state'        => 'sometimes',
            'zip_code'     => 'sometimes',
            'country'      => 'sometimes',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'error'   => true,
                'message' => 'Validation failed',
                'records' => $validator->errors()
            ], 200);
        }

        $player = Player::where('id', $request->player_ID)->first();

        if (!$player) {
            return response()->json([
                'error'   => true,
                'message' => 'Player not found with ID: ' . $request->player_ID,
            ], 200);
        }

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
            'message' => 'Player'.' ID:' . $request->player_ID . ' updated successfully'. ' by ' . 'Admin',
            'records' => $player
        ], 200);
    }
}
