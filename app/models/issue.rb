class Issue < ActiveRecord::Base
  attr_accessible :is_published, :number, :season, :title, :description
  has_many :pieces
  has_many :authors, :through => :pieces
  validates_presence_of :number, :title, :season, :is_published
end
