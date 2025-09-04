<?php

namespace App\Http\Controllers\Team;

use App\HelperFunctions\HelperFunctions;
use App\Http\Controllers\Controller;
use App\Models\Club;
use App\Models\Coach;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use App\Models\Team;

class TeamController extends Controller
{
    public function addTeam(Request $request)
    {

        $validated = $request->validate([
            'name'        => 'required|string|max:255',
            'sport_type'  => 'required|string|max:255',
            'club_id'     => 'nullable',
            'coach_id'    => 'nullable',
            'level'       => 'nullable|string|max:255',
            'city' => 'required|string|max:255',
            'country' => 'required|string|max:255',
            'founded_year' => 'required|integer',
            'description' => 'required|string|max:1000',
            'team_logo' => 'nullable',
        ]);

        // Check if club_id exists if provided
        if (!empty($validated['club_id'])) {
            $clubExists = Club::where('id', $validated['club_id'])->exists();
            if (!$clubExists) {
                return response()->json([
                    'error' => true,
                    'message' => 'Club Id not found',
                ], 200);
            }
        }

        // Check if coach_id exists if provided
        if (!empty($validated['coach_id'])) {
            $coachExists = Coach::where('id', $validated['coach_id'])->exists();
            if (!$coachExists) {
                return response()->json([
                    'error' => true,
                    'message' => 'Coach Id not found',
                ], 200);
            }
        }

        try {

            $team = Team::create($validated);

            if ($request->hasFile('team_logo')) {
                $validated['team_logo'] = HelperFunctions::uploadImage($request->file('team_logo'), 'teams');
                $team->team_logo = $validated['team_logo'];
                $team->save();
            }
        } catch (\Exception $e) {
            return response()->json([
                'error'   => true,
                'message' => 'Error creating team: ' . $e->getMessage(),
            ], 200);
        }


        return response()->json([
            'error'   => false,
            'message' => $team->name . ' Team created successfully' . ' by ' . 'Admin',
            'records' => $team
        ], 200);
    }

    public function editTeam(Request $request)
    {
        $validated = $request->validate([
            'team_id'     => 'required',
            'name'        => 'nullable',
            'club_id'     => 'nullable',
            'coach_id'    => 'nullable',
            'level'       => 'sometimes',
            'city' => 'sometimes',
            'country' => 'sometimes',
            'founded_year' => 'sometimes',
            'description' => 'sometimes',
            'team_logo' => 'nullable',
        ]);

        $team = Team::where('id', $validated['team_id'])->first();

        if (!$team) {
            return response()->json([
                'error'   => true,
                'message' => 'Team not found with ID: ' . $validated['team_id'],
            ], 200);
        }

        unset($validated['team_id']);

        if (isset($validated['team_logo'])) {
            $validated['team_logo'] = HelperFunctions::uploadImage($request->file('team_logo'), 'teams');
            $team->team_logo = $validated['team_logo'];
            $team->save();
        }

        $team->update($validated);

        return response()->json([
            'error'   => false,
            'message' => $team->name . ' Team updated successfully' . ' by ' . 'Admin',
            'records' => $team
        ], 200);
    }

    public function deleteTeam(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'team_id' => 'required',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'error'   => true,
                'message' => 'Validation failed',
                'records' => $validator->errors()
            ], 200);
        }

        $team = Team::where('id', $request->team_id)->first();

        if (!$team) {
            return response()->json([
                'error'   => true,
                'message' => 'Team not found with ID: ' . $request->team_id,
            ], 200);
        }
        $team->delete();

        return response()->json([
            'error'   => false,
            'message' => 'Team deleted successfully: ' . $request->team_id . ' by ' . 'Admin',
        ], 200);
    }

    public function getAllTeams(Request $request)
    {
        $teams = Team::all();

        if (!$teams || $teams->isEmpty()) {
            return response()->json([
                'error'   => true,
                'message' => 'No teams found'
            ], 200);
        }

        return response()->json([
            'error'   => false,
            'message' => 'All teams fetched successfully',
            'records' => $teams
        ], 200);
    }
}
