<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('teams', function (Blueprint $table) {
            $table->id();
            $table->string('name', 255);
            $table->string('sport_type', 255);
            $table->unsignedBigInteger('club_id')->nullable();
            $table->unsignedBigInteger('coach_id')->nullable();
            $table->string('level', 255)->nullable();
            $table->timestamps();

            // Optional foreign keys (if you already have clubs & coaches tables)
            $table->foreign('club_id')->references('id')->on('clubs')->onDelete('set null');
            $table->foreign('coach_id')->references('id')->on('coaches')->onDelete('set null');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('teams');
    }
};
