<?php

namespace App\Http\Controllers\Club;

use App\HelperFunctions\HelperFunctions;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use App\Models\Club;
use App\Models\Coach;
use App\Models\Team;
use Illuminate\Support\Facades\Log;

class ClubController extends Controller
{
    public function clubRegister(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'name'     => 'required|string|max:100',
            'email'    => 'required',
            'password' => 'required|string|min:6|max:100',
            'phone'    => 'required|string|max:100',
            'address'  => 'required|string|max:255',
            'city'     => 'required|string|max:100',
            'country'  => 'required|string|max:100',
            'sport_type' => 'required|string|max:100',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'error'   => true,
                'message' => 'Validation Error',
                'records' => $validator->errors()
            ], 200);
        }

        $club = Club::create([
            'name'     => $request->name,
            'email'    => $request->email,
            'password' => Hash::make($request->password),
            'phone_number'    => $request->phone,
            'address'  => $request->address,
            'city'     => $request->city,
            'country'  => $request->country,
            'sport_type' => $request->sport_type,
        ]);

        return response()->json([
            'error'   => false,
            'message' => 'Club registered successfully',
            'records' => $club
        ], 200);
    }

    public function clubLogin(Request $request)
    {
        $request->validate([
            'email'    => 'required|email',
            'password' => 'required|string'
        ]);

        $club = Club::where('email', $request->email)->first();

        if (!$club) {
            return response()->json([
                'error'   => true,
                'message' => 'Club Email not found',
                'records' => $request->email
            ], 200);
        }

        if (!Hash::check($request->password, $club->password)) {
            return response()->json([
                'error'   => true,
                'message' => 'Password does not match'
            ], 200);
        }

        $token = $club->createToken('club-token')->plainTextToken;

        return response()->json([
            'error'   => false,
            'message' => 'Club Login successful',
            'token'   => $token,
            'records' => $club
        ], 200);
    }

    public function addClub(Request $request)
    {
        try {

            $validated = $request->validate([
                'name'          => 'required|string|max:100',
                'email'         => 'required',
                'password'      => 'required|string|min:6',
                'address'       => 'required',
                'phone'  => 'required',
                'location'      => 'nullable',
                'coach_id'      => 'nullable',
                'team_id'      => 'nullable',
                'profile_image' => 'nullable',
                'sport_type'    => 'required|in:cricket,football',

            ]);

            // Check if email already exists
            $emailExists = Club::where('email', $validated['email'])->exists();
            if ($emailExists) {
                return response()->json([
                    'error' => true,
                    'message' => 'Email already exists: ' . $validated['email'],
                ], 200);
            }

            // Check if coach_id exists if provided
            if (!empty($validated['coach_id'])) {
                $coachExists = Coach::where('id', $validated['coach_id'])->exists();
                if (!$coachExists) {
                    return response()->json([
                        'error' => true,
                        'message' => 'Coach not found with ID: ' . $validated['coach_id'],
                    ], 200);
                }
            }

            // Check if team_id exists if provided
            if (!empty($validated['team_id'])) {
                $teamExists = Team::where('id', $validated['team_id'])->exists();
                if (!$teamExists) {
                    return response()->json([
                        'error' => true,
                        'message' => 'Team not found with ID: ' . $validated['team_id'],
                    ], 200);
                }
            }
            // Handle image upload
            $profileImagePath = null;
            if ($request->hasFile('profile_image')) {
                $profileImagePath = HelperFunctions::uploadImage($request->file('profile_image'), 'clubs');
            }

            $club = Club::create([
                'name' => $validated['name'],
                'email' => $validated['email'],
                'password' => Hash::make($validated['password']),
                'address' => $validated['address'],
                'phone_number' => $validated['phone'],
                'location' => $validated['location'] ?? null,
                'coach_id' => $validated['coach_id'] ?? null,
                'team_id' => $validated['team_id'] ?? null,
                'profile_image' => $profileImagePath,
                'sport_type' => $validated['sport_type'],
            ]);

            return response()->json([
                'error'   => false,
                'message' => 'Club created successfully',
                'records' => $club
            ], 200);
        } catch (\Throwable $e) {
            return response()->json([
                'error'   => true,
                'message' => 'Error creating club: ' . $e->getMessage(),
            ], 200);
        }
    }

    public function editClub(Request $request)
    {
        try {
            $validated = $request->validate([
                'club_id'      => 'required',
                'name'         => 'sometimes|string',
                'email'        => 'sometimes',
                'password'     => 'sometimes|string|min:6',
                'address'      => 'sometimes|string',
                'phone'        => 'sometimes|string',
                'location'     => 'sometimes|string',
                'coach_id'     => 'sometimes',
                'team_id'      => 'sometimes',
                'profile_image' => 'sometimes',
                'sport_type'    => 'sometimes|string',
                'city'         => 'sometimes|string',
                'country'      => 'sometimes|string'
            ]);

            $club = Club::where('id', $validated['club_id'])->first();

            if (!$club) {
                return response()->json([
                    'error'   => true,
                    'message' => 'Club not found with ID: ' . $validated['club_id']
                ], 200);
            }

            if (isset($validated['password'])) {
                $validated['password'] = Hash::make($validated['password']);
            }

            if ($request->hasFile('profile_image')) {
                $validated['profile_image'] = HelperFunctions::uploadImage($request->file('profile_image'), 'clubs');
                $club->profile_image = $validated['profile_image'];
                $club->save();
            }

            unset($validated['club_id']);

            // Map phone to phone_number for database column
            if (isset($validated['phone'])) {
                $validated['phone_number'] = $validated['phone'];
                unset($validated['phone']);
            }

            $club->update($validated);

            return response()->json([
                'error' => false,
                'message' => 'Club ID: ' . $request->club_id . ' updated successfully',
                'records' => $club
            ], 200);

        } catch (\Exception $e) {
            return response()->json([
                'error' => true,
                'message' => 'An error occurred while updating the club: ' . $e->getMessage()
            ], 500);
        }
    }

    public function deleteClub(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'club_id' => 'required',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'error'   => true,
                'message' => 'Validation failed',
                'records' => $validator->errors()
            ], 200);
        }

        $club = Club::where('id', $request->club_id)->first();

        if (!$club) {
            return response()->json([
                'error'   => true,
                'message' => 'Club not found with ID: ' . $request->club_id
            ], 200);
        }

        $club->delete();

        return response()->json([
            'error'   => false,
            'message' => 'Club ID: ' . $request->club_id . ' deleted successfully',
        ], 200);
    }

    public function getAllClubs(Request $request)
    {
        $clubs = Club::all();

        if (!$clubs || $clubs->isEmpty()) {
            return response()->json([
                'error'   => true,
                'message' => 'No clubs found'
            ], 200);
        }
        return response()->json([
            'error'   => false,
            'message' => 'All clubs fetched successfully',
            'records' => $clubs
        ], 200);
    }
}
